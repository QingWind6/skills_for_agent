import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readFile, writeFile, stat, readdir } from "node:fs/promises";
import { createReadStream } from "node:fs";
import { spawn } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const APP_DIR = __dirname;
const PUBLIC_DIR = path.join(APP_DIR, "public");
const EXPORT_DIR = path.join(APP_DIR, "exports");
const DECK_FILE = path.join(APP_DIR, "deck.json");
const PORT = Number(process.env.PORT || 43210);

const MIME_TYPES = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".mjs": "application/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8"
};

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload, null, 2));
}

function sendText(res, statusCode, text) {
  res.writeHead(statusCode, { "Content-Type": "text/plain; charset=utf-8" });
  res.end(text);
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}

function normalizeDeck(deck) {
  if (!deck || typeof deck !== "object" || !Array.isArray(deck.cards)) {
    throw new Error("Invalid deck payload");
  }
  return {
    meta: {
      title: deck.meta?.title || "未命名卡片集",
      subtitle: deck.meta?.subtitle || "",
      templateId: deck.meta?.templateId || "editorial-tech",
      aspectRatio: deck.meta?.aspectRatio || "3:4",
      updatedAt: new Date().toISOString()
    },
    cards: deck.cards
  };
}

async function listExports() {
  const dirents = await readdir(EXPORT_DIR, { withFileTypes: true }).catch(() => []);
  const runs = [];

  for (const dirent of dirents) {
    if (!dirent.isDirectory()) continue;
    const runDir = path.join(EXPORT_DIR, dirent.name);
    const files = (await readdir(runDir)).filter((file) => file.endsWith(".png")).sort();
    runs.push({
      id: dirent.name,
      path: `/exports/${dirent.name}/`,
      files: files.map((file) => ({
        name: file,
        href: `/exports/${dirent.name}/${file}`
      }))
    });
  }

  runs.sort((a, b) => b.id.localeCompare(a.id));
  return runs.slice(0, 10);
}

async function serveFile(res, filePath) {
  try {
    const fileStat = await stat(filePath);
    if (!fileStat.isFile()) {
      sendText(res, 404, "Not found");
      return;
    }
    const ext = path.extname(filePath);
    const mimeType = MIME_TYPES[ext] || "application/octet-stream";
    res.writeHead(200, {
      "Content-Type": mimeType,
      "Cache-Control": "no-store"
    });
    createReadStream(filePath).pipe(res);
  } catch {
    sendText(res, 404, "Not found");
  }
}

async function runExport() {
  return await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ["export.mjs"], {
      cwd: APP_DIR,
      env: {
        ...process.env,
        PORT: String(PORT)
      },
      stdio: ["ignore", "pipe", "pipe"]
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(stderr || stdout || `Export failed with code ${code}`));
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch (error) {
        reject(new Error(`Failed to parse export output: ${error.message}\n${stdout}`));
      }
    });
  });
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", `http://${req.headers.host}`);

    if (req.method === "GET" && url.pathname === "/api/health") {
      sendJson(res, 200, { ok: true, port: PORT });
      return;
    }

    if (req.method === "GET" && url.pathname === "/api/deck") {
      const deck = JSON.parse(await readFile(DECK_FILE, "utf8"));
      sendJson(res, 200, deck);
      return;
    }

    if (req.method === "POST" && url.pathname === "/api/deck") {
      const body = await readBody(req);
      const normalized = normalizeDeck(JSON.parse(body));
      await writeFile(DECK_FILE, `${JSON.stringify(normalized, null, 2)}\n`, "utf8");
      sendJson(res, 200, { ok: true, updatedAt: normalized.meta.updatedAt });
      return;
    }

    if (req.method === "GET" && url.pathname === "/api/exports") {
      sendJson(res, 200, { runs: await listExports() });
      return;
    }

    if (req.method === "POST" && url.pathname === "/api/export") {
      const result = await runExport();
      sendJson(res, 200, { ok: true, ...result, runs: await listExports() });
      return;
    }

    if (url.pathname.startsWith("/exports/")) {
      await serveFile(res, path.join(APP_DIR, url.pathname));
      return;
    }

    if (url.pathname === "/" || url.pathname === "/index.html") {
      await serveFile(res, path.join(PUBLIC_DIR, "index.html"));
      return;
    }

    await serveFile(res, path.join(PUBLIC_DIR, url.pathname));
  } catch (error) {
    sendJson(res, 500, {
      ok: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`xhs-card-studio-prototype running at http://127.0.0.1:${PORT}`);
});
