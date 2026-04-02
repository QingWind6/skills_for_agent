import path from "node:path";
import { fileURLToPath } from "node:url";
import { mkdir, writeFile } from "node:fs/promises";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT || 43210);
const EXPORT_ROOT = path.join(__dirname, "exports");
const chromePath = process.env.CHROME_PATH || "/usr/bin/google-chrome";

function timestamp() {
  const now = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  return [
    now.getFullYear(),
    pad(now.getMonth() + 1),
    pad(now.getDate())
  ].join("") + "-" + [
    pad(now.getHours()),
    pad(now.getMinutes()),
    pad(now.getSeconds())
  ].join("");
}

const runId = timestamp();
const runDir = path.join(EXPORT_ROOT, runId);
await mkdir(runDir, { recursive: true });

const browser = await chromium.launch({
  executablePath: chromePath,
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"]
});

try {
  const page = await browser.newPage({
    viewport: { width: 1800, height: 1600 },
    deviceScaleFactor: 2
  });
  await page.goto(`http://127.0.0.1:${PORT}/?mode=export`, {
    waitUntil: "networkidle"
  });
  await page.waitForFunction(() => window.__APP_READY__ === true);
  const layoutIssues = await page.evaluate(() => window.__LAYOUT_ISSUES__ || []);
  if (layoutIssues.length) {
    throw new Error(`Export blocked by layout issues: ${JSON.stringify(layoutIssues)}`);
  }

  const cards = page.locator(".card-frame");
  const count = await cards.count();
  const files = [];

  for (let index = 0; index < count; index += 1) {
    const card = cards.nth(index);
    const exportName = (await card.getAttribute("data-export-name")) || `card-${index + 1}`;
    const filename = `${String(index + 1).padStart(2, "0")}-${exportName}.png`;
    const fullPath = path.join(runDir, filename);
    await card.screenshot({ path: fullPath });
    files.push(filename);
  }

  await writeFile(
    path.join(runDir, "manifest.json"),
    `${JSON.stringify({ runId, files }, null, 2)}\n`,
    "utf8"
  );

  process.stdout.write(JSON.stringify({
    runId,
    runPath: `/exports/${runId}/`,
    files
  }));
} finally {
  await browser.close();
}
