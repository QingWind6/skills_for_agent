import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import readline from 'node:readline';
import { mkdir, readFile, readdir, stat, writeFile } from 'node:fs/promises';

import { GeminiClient, GeneratedImage, Model, type Image as GeminiImage, type ModelOutput } from './gemini-webapi/index.js';
import { resolveGeminiWebChromeProfileDir, resolveGeminiWebConsentPath, resolveGeminiWebCookiePath, resolveGeminiWebSessionPath, resolveGeminiWebSessionsDir } from './gemini-webapi/utils/index.js';

type CliArgs = {
  prompt: string | null;
  promptFiles: string[];
  modelId: string;
  mode: 'auto' | 'text' | 'image';
  json: boolean;
  imagePath: string | null;
  rawJsonPath: string | null;
  referenceImages: string[];
  sessionId: string | null;
  listSessions: boolean;
  login: boolean;
  acceptDisclaimer: boolean;
  cookiePath: string | null;
  profileDir: string | null;
  timeoutSeconds: number | null;
  autoImagePrompt: boolean;
  stageLogs: boolean;
  help: boolean;
};

type SessionRecord = {
  id: string;
  metadata: Array<string | null>;
  messages: Array<{ role: 'user' | 'assistant'; content: string; timestamp: string; error?: string }>;
  createdAt: string;
  updatedAt: string;
};

type ConsentRecord = {
  version: number;
  accepted: true;
  acceptedAt: string;
  disclaimerVersion: string;
};

type SelectedImage = {
  image: GeminiImage;
  candidateIndex: number;
  imageIndex: number;
};

type LegacySessionV1 = {
  version?: number;
  sessionId?: string;
  updatedAt?: string;
  conversationId?: string | null;
  responseId?: string | null;
  choiceId?: string | null;
  chatMetadata?: unknown;
};

const DISCLAIMER_VERSION = '1.0';
const IMAGE_PROMPT_PREFIX = [
  'Generate exactly one standalone image.',
  'Return an image result, not a text-only answer.',
];

function normalizeSessionMetadata(input: unknown): Array<string | null> {
  if (Array.isArray(input)) {
    const out: Array<string | null> = [];
    for (const v of input.slice(0, 3)) out.push(typeof v === 'string' ? v : null);
    return out.length > 0 ? out : [null, null, null];
  }

  if (input && typeof input === 'object') {
    const v1 = input as LegacySessionV1;
    if (Array.isArray(v1.chatMetadata)) return normalizeSessionMetadata(v1.chatMetadata);

    const conv = typeof v1.conversationId === 'string' ? v1.conversationId : null;
    const rid = typeof v1.responseId === 'string' ? v1.responseId : null;
    const rcid = typeof v1.choiceId === 'string' ? v1.choiceId : null;
    if (conv || rid || rcid) return [conv, rid, rcid];
  }

  return [null, null, null];
}

function formatScriptCommand(fallback: string): string {
  const raw = process.argv[1];
  const displayPath = raw
    ? (() => {
        const relative = path.relative(process.cwd(), raw);
        return relative && !relative.startsWith("..") ? relative : raw;
      })()
    : fallback;
  const quotedPath = displayPath.includes(" ")
    ? `"${displayPath.replace(/"/g, '\\"')}"`
    : displayPath;
  return `npx -y bun ${quotedPath}`;
}

function printUsage(cookiePath: string, profileDir: string): void {
  const cmd = formatScriptCommand("scripts/main.ts");
  console.log(`Usage:
  ${cmd} --prompt "A cute cat astronaut" --image generated.png
  ${cmd} --promptfiles system.md content.md --image out.png
  ${cmd} --mode image --prompt "A cute cat" --image generated.png
  ${cmd} --prompt "Create a variation" --reference reference.png --image variant.png
  ${cmd} --prompt "A cute cat" --image generated.png --raw-json generated.response.json

Login / consent:
  ${cmd} --login
  ${cmd} --login --accept-disclaimer

Text diagnostics:
  ${cmd} --mode text --prompt "Hello" --json

Options:
  -p, --prompt <text>       Prompt text
  --promptfiles <files...>  Read prompt from one or more files (concatenated in order)
  -m, --model <id>          gemini-3-pro | gemini-3-flash | gemini-3-flash-thinking | gemini-3.1-pro-preview (default: gemini-3-pro)
  --mode <kind>             auto | text | image (default: auto; --image implies image mode)
  --json                    Output JSON
  --image [path]            Generate an image and save it (default: ./generated.png)
  --raw-json <path>         Save parsed response JSON for debugging (default: <image>.response.json)
  --reference <files...>    Reference images for vision input
  --ref <files...>          Alias for --reference
  --sessionId <id>          Session ID for multi-turn conversation (agent should generate unique ID)
  --list-sessions           List saved sessions (max 100, sorted by update time)
  --login                   Only refresh cookies, then exit
  --accept-disclaimer       Record consent non-interactively for first use
  --cookie-path <path>      Cookie file path (default: ${cookiePath})
  --profile-dir <path>      Chrome profile dir (default: ${profileDir})
  --timeout <seconds>       Request timeout in seconds (default: 300 text, 420 image)
  --no-auto-image-prompt    Do not inject the explicit image-generation wrapper prompt
  --quiet-stages            Suppress stage logs on stderr
  -h, --help                Show help

Env overrides:
  GEMINI_WEB_DATA_DIR, GEMINI_WEB_COOKIE_PATH, GEMINI_WEB_CHROME_PROFILE_DIR, GEMINI_WEB_CHROME_PATH, GEMINI_WEB_ACCEPT_DISCLAIMER

Notes:
  First login uses this skill's dedicated Chrome profile directory.
  --image implies image mode and also writes <image>.response.json by default.`);
}

function parseArgs(argv: string[]): CliArgs {
  const out: CliArgs = {
    prompt: null,
    promptFiles: [],
    modelId: 'gemini-3-pro',
    mode: 'auto',
    json: false,
    imagePath: null,
    rawJsonPath: null,
    referenceImages: [],
    sessionId: null,
    listSessions: false,
    login: false,
    acceptDisclaimer: false,
    cookiePath: null,
    profileDir: null,
    timeoutSeconds: null,
    autoImagePrompt: true,
    stageLogs: true,
    help: false,
  };

  const positional: string[] = [];

  const takeMany = (i: number): { items: string[]; next: number } => {
    const items: string[] = [];
    let j = i + 1;
    while (j < argv.length) {
      const v = argv[j]!;
      if (v.startsWith('-')) break;
      items.push(v);
      j++;
    }
    return { items, next: j - 1 };
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === '--help' || a === '-h') {
      out.help = true;
      continue;
    }

    if (a === '--json') {
      out.json = true;
      continue;
    }

    if (a === '--quiet-stages') {
      out.stageLogs = false;
      continue;
    }

    if (a === '--list-sessions') {
      out.listSessions = true;
      continue;
    }

    if (a === '--login') {
      out.login = true;
      continue;
    }

    if (a === '--accept-disclaimer') {
      out.acceptDisclaimer = true;
      continue;
    }

    if (a === '--prompt' || a === '-p') {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.prompt = v;
      continue;
    }

    if (a === '--promptfiles') {
      const { items, next } = takeMany(i);
      if (items.length === 0) throw new Error('Missing files for --promptfiles');
      out.promptFiles.push(...items);
      i = next;
      continue;
    }

    if (a === '--model' || a === '-m') {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.modelId = v;
      continue;
    }

    if (a === '--mode') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --mode');
      if (v !== 'auto' && v !== 'text' && v !== 'image') {
        throw new Error(`Invalid --mode value: ${v}`);
      }
      out.mode = v;
      continue;
    }

    if (a === '--sessionId') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --sessionId');
      out.sessionId = v;
      continue;
    }

    if (a === '--cookie-path') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --cookie-path');
      out.cookiePath = v;
      continue;
    }

    if (a === '--profile-dir') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --profile-dir');
      out.profileDir = v;
      continue;
    }

    if (a === '--raw-json') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --raw-json');
      out.rawJsonPath = v;
      continue;
    }

    if (a === '--timeout') {
      const v = argv[++i];
      if (!v) throw new Error('Missing value for --timeout');
      if (!/^\d+$/.test(v)) {
        throw new Error(`Invalid --timeout value: ${v}`);
      }
      const parsed = Number.parseInt(v, 10);
      if (!Number.isFinite(parsed) || parsed <= 0) throw new Error(`Invalid --timeout value: ${v}`);
      out.timeoutSeconds = parsed;
      continue;
    }

    if (a === '--no-auto-image-prompt') {
      out.autoImagePrompt = false;
      continue;
    }

    if (a === '--image' || a.startsWith('--image=')) {
      let v: string | null = null;
      if (a.startsWith('--image=')) {
        v = a.slice('--image='.length).trim();
      } else {
        const maybe = argv[i + 1];
        if (maybe && !maybe.startsWith('-')) {
          v = maybe;
          i++;
        }
      }

      out.imagePath = v && v.length > 0 ? v : 'generated.png';
      continue;
    }

    if (a === '--reference' || a === '--ref') {
      const { items, next } = takeMany(i);
      if (items.length === 0) throw new Error(`Missing files for ${a}`);
      out.referenceImages.push(...items);
      i = next;
      continue;
    }

    if (a.startsWith('-')) {
      throw new Error(`Unknown option: ${a}`);
    }

    positional.push(a);
  }

  if (!out.prompt && out.promptFiles.length === 0 && positional.length > 0) {
    out.prompt = positional.join(' ');
  }

  return out;
}

function resolveModel(id: string): Model {
  const k = id.trim();
  if (k === 'gemini-3-pro') return Model.G_3_0_PRO;
  if (k === 'gemini-3.0-pro') return Model.G_3_0_PRO;
  if (k === 'gemini-3-flash') return Model.G_3_0_FLASH;
  if (k === 'gemini-3.0-flash') return Model.G_3_0_FLASH;
  if (k === 'gemini-3-flash-thinking') return Model.G_3_0_FLASH_THINKING;
  if (k === 'gemini-3.0-flash-thinking') return Model.G_3_0_FLASH_THINKING;
  if (k === 'gemini-3.1-pro-preview') return Model.G_3_1_PRO_PREVIEW;
  return Model.from_name(k);
}

async function readPromptFromFiles(files: string[]): Promise<string> {
  const parts: string[] = [];
  for (const f of files) {
    parts.push(await readFile(f, 'utf8'));
  }
  return parts.join('\n\n');
}

async function readPromptFromStdin(): Promise<string | null> {
  if (process.stdin.isTTY) return null;
  try {
    // Bun provides Bun.stdin; Node-compatible read can be flaky across runtimes.
    const t = await Bun.stdin.text();
    const v = t.trim();
    return v.length > 0 ? v : null;
  } catch {
    return null;
  }
}

function normalizeOutputImagePath(p: string): string {
  const full = path.resolve(p);
  const ext = path.extname(full);
  if (ext) return full;
  return `${full}.png`;
}

function normalizeJsonPath(p: string): string {
  const full = path.resolve(p);
  return full.endsWith('.json') ? full : `${full}.json`;
}

function inferMode(args: CliArgs): 'text' | 'image' {
  if (args.mode === 'text' || args.mode === 'image') return args.mode;
  return args.imagePath ? 'image' : 'text';
}

function defaultTimeoutSeconds(mode: 'text' | 'image'): number {
  return mode === 'image' ? 420 : 300;
}

function buildImagePrompt(prompt: string): string {
  return [
    ...IMAGE_PROMPT_PREFIX,
    'Do not ask follow-up questions.',
    'Do not render any text in the image unless the prompt explicitly asks for text.',
    prompt.trim(),
  ].join('\n\n');
}

function hasImagePromptWrapper(prompt: string): boolean {
  const normalized = prompt.trimStart().replace(/\r\n/g, '\n');
  return normalized.startsWith(IMAGE_PROMPT_PREFIX.join('\n\n'));
}

function normalizePromptForMode(prompt: string, mode: 'text' | 'image', autoImagePrompt: boolean): string {
  if (mode !== 'image' || !autoImagePrompt) return prompt;
  if (hasImagePromptWrapper(prompt)) return prompt;
  return buildImagePrompt(prompt);
}

function defaultRawJsonPath(imagePath: string): string {
  return `${normalizeOutputImagePath(imagePath)}.response.json`;
}

function logStage(enabled: boolean, stage: string, message: string): void {
  if (!enabled) return;
  console.error(`[gemini-web-image:${stage}] ${message}`);
}

function isTruthyEnv(value: string | undefined): boolean {
  if (!value) return false;
  const normalized = value.trim().toLowerCase();
  return normalized === '1' || normalized === 'true' || normalized === 'yes';
}

async function promptYesNo(question: string): Promise<boolean> {
  if (!process.stdin.isTTY) return false;

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stderr,
  });

  try {
    const answer = await new Promise<string>((resolve) => rl.question(question, resolve));
    const normalized = answer.trim().toLowerCase();
    return normalized === 'y' || normalized === 'yes';
  } finally {
    rl.close();
  }
}

function isValidConsent(value: unknown): value is ConsentRecord {
  if (!value || typeof value !== 'object') return false;
  const record = value as Partial<ConsentRecord>;
  return (
    record.accepted === true &&
    record.disclaimerVersion === DISCLAIMER_VERSION &&
    typeof record.acceptedAt === 'string' &&
    record.acceptedAt.length > 0
  );
}

async function ensureConsent(autoAccept: boolean, stageLogs: boolean): Promise<void> {
  const consentPath = resolveGeminiWebConsentPath();

  try {
    if (fs.existsSync(consentPath) && fs.statSync(consentPath).isFile()) {
      const raw = await readFile(consentPath, 'utf8');
      const parsed = JSON.parse(raw) as unknown;
      if (isValidConsent(parsed)) {
        logStage(stageLogs, 'consent', `Reverse-engineered Gemini Web access accepted on ${(parsed as ConsentRecord).acceptedAt}`);
        return;
      }
    }
  } catch {
    // Fall through to prompt or explicit accept.
  }

  const disclaimer = [
    'WARNING: This tool uses a reverse-engineered Gemini Web workflow, not the official API.',
    'Risks:',
    '- Google may change the web flow without notice.',
    '- There is no official support or stability guarantee.',
    '- Use may require manual Google or Gemini web login steps.',
    '- Use at your own risk.',
  ].join('\n');

  console.error(disclaimer);

  const accepted = autoAccept || isTruthyEnv(process.env.GEMINI_WEB_ACCEPT_DISCLAIMER)
    ? true
    : await promptYesNo('Do you accept these terms and wish to continue? (y/N): ');

  if (!accepted) {
    throw new Error(
      `Consent required. Rerun with --accept-disclaimer or create ${consentPath} with accepted: true and disclaimerVersion: ${DISCLAIMER_VERSION}`,
    );
  }

  await mkdir(path.dirname(consentPath), { recursive: true });
  const payload: ConsentRecord = {
    version: 1,
    accepted: true,
    acceptedAt: new Date().toISOString(),
    disclaimerVersion: DISCLAIMER_VERSION,
  };
  await writeFile(consentPath, JSON.stringify(payload, null, 2), 'utf8');
  logStage(stageLogs, 'consent', `Saved consent to ${consentPath}`);
}

async function loadSession(id: string): Promise<SessionRecord | null> {
  const p = resolveGeminiWebSessionPath(id);
  try {
    const raw = await readFile(p, 'utf8');
    const j = JSON.parse(raw) as unknown;
    if (!j || typeof j !== 'object') return null;

    const sid = (typeof (j as any).id === 'string' && (j as any).id.trim()) || (typeof (j as any).sessionId === 'string' && (j as any).sessionId.trim()) || id;
    const metadata = normalizeSessionMetadata((j as any).metadata ?? (j as any).chatMetadata ?? j);
    const messages = Array.isArray((j as any).messages) ? ((j as any).messages as SessionRecord['messages']) : [];
    const createdAt =
      typeof (j as any).createdAt === 'string'
        ? ((j as any).createdAt as string)
        : typeof (j as any).updatedAt === 'string'
          ? ((j as any).updatedAt as string)
          : new Date().toISOString();
    const updatedAt = typeof (j as any).updatedAt === 'string' ? ((j as any).updatedAt as string) : createdAt;

    return {
      id: sid,
      metadata,
      messages,
      createdAt,
      updatedAt,
    };
  } catch {
    return null;
  }
}

async function saveSession(rec: SessionRecord): Promise<void> {
  const dir = resolveGeminiWebSessionsDir();
  await mkdir(dir, { recursive: true });
  const p = resolveGeminiWebSessionPath(rec.id);
  const tmp = `${p}.tmp.${Date.now()}`;
  await writeFile(tmp, JSON.stringify(rec, null, 2), 'utf8');
  await fs.promises.rename(tmp, p);
}

async function listSessions(): Promise<SessionRecord[]> {
  const dir = resolveGeminiWebSessionsDir();
  try {
    const names = await readdir(dir);
    const items: Array<{ path: string; st: number }> = [];
    for (const n of names) {
      if (!n.endsWith('.json')) continue;
      const p = path.join(dir, n);
      try {
        const s = await stat(p);
        items.push({ path: p, st: s.mtimeMs });
      } catch {}
    }

    items.sort((a, b) => b.st - a.st);
    const out: SessionRecord[] = [];
    for (const it of items.slice(0, 100)) {
      try {
        const raw = await readFile(it.path, 'utf8');
        const j = JSON.parse(raw) as any;
        const id =
          (typeof j?.id === 'string' && j.id.trim()) ||
          (typeof j?.sessionId === 'string' && j.sessionId.trim()) ||
          path.basename(it.path, '.json');
        out.push({
          id,
          metadata: normalizeSessionMetadata(j?.metadata ?? j?.chatMetadata ?? j),
          messages: Array.isArray(j?.messages) ? j.messages : [],
          createdAt:
            typeof j?.createdAt === 'string'
              ? j.createdAt
              : typeof j?.updatedAt === 'string'
                ? j.updatedAt
                : new Date(it.st).toISOString(),
          updatedAt: typeof j?.updatedAt === 'string' ? j.updatedAt : new Date(it.st).toISOString(),
        });
      } catch {}
    }

    out.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));
    return out.slice(0, 100);
  } catch {
    return [];
  }
}

function formatJson(out: ModelOutput, extra?: Record<string, unknown>): string {
  const candidates = out.candidates.map((c) => ({
    rcid: c.rcid,
    text: c.text,
    thoughts: c.thoughts,
    images: c.images.map((img) => ({
      url: img.url,
      title: img.title,
      alt: img.alt,
      kind: img instanceof GeneratedImage ? 'generated' : 'web',
    })),
  }));

  return JSON.stringify(
    {
      text: out.text,
      thoughts: out.thoughts,
      metadata: out.metadata,
      chosen: out.chosen,
      candidates,
      ...extra,
    },
    null,
    2,
  );
}

function selectOutputImage(out: ModelOutput): SelectedImage | null {
  const ordered = [out.chosen, ...out.candidates.map((_, index) => index)];
  const seen = new Set<number>();

  for (const candidateIndex of ordered) {
    if (seen.has(candidateIndex)) continue;
    seen.add(candidateIndex);

    const candidate = out.candidates[candidateIndex];
    if (!candidate?.images?.length) continue;

    return {
      image: candidate.images[0]!,
      candidateIndex,
      imageIndex: 0,
    };
  }

  return null;
}

async function writeResponseDebugJson(
  rawJsonPath: string,
  out: ModelOutput | null,
  extra: Record<string, unknown>,
): Promise<void> {
  await mkdir(path.dirname(rawJsonPath), { recursive: true });
  const payload = out ? formatJson(out, extra) : JSON.stringify(extra, null, 2);
  await writeFile(rawJsonPath, payload, 'utf8');
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.cookiePath) process.env.GEMINI_WEB_COOKIE_PATH = args.cookiePath;
  if (args.profileDir) process.env.GEMINI_WEB_CHROME_PROFILE_DIR = args.profileDir;

  const cookiePath = resolveGeminiWebCookiePath();
  const profileDir = resolveGeminiWebChromeProfileDir();

  if (args.help) {
    printUsage(cookiePath, profileDir);
    return;
  }

  if (args.listSessions) {
    const ss = await listSessions();
    for (const s of ss) {
      const n = s.messages.length;
      const last = s.messages.slice(-1)[0];
      const lastLine = last?.content ? String(last.content).split('\n')[0] : '';
      console.log(`${s.id}\t${s.updatedAt}\t${n}\t${lastLine}`);
    }
    return;
  }

  if (args.login) {
    await ensureConsent(args.acceptDisclaimer, args.stageLogs);
    process.env.GEMINI_WEB_LOGIN = '1';
    const c = new GeminiClient();
    await c.init({ verbose: true });
    await c.close();
    if (!args.json) console.log(`Cookie refreshed: ${cookiePath}`);
    else console.log(JSON.stringify({ ok: true, cookiePath }, null, 2));
    return;
  }

  let prompt: string | null = args.prompt;
  if (!prompt && args.promptFiles.length > 0) prompt = await readPromptFromFiles(args.promptFiles);
  if (!prompt) prompt = await readPromptFromStdin();

  if (!prompt) {
    printUsage(cookiePath, profileDir);
    process.exitCode = 1;
    return;
  }

  const mode = inferMode(args);
  if (mode === 'image' && !args.imagePath) {
    throw new Error('--image is required when mode=image');
  }

  const effectivePrompt = normalizePromptForMode(prompt, mode, args.autoImagePrompt);
  const timeoutSeconds = args.timeoutSeconds ?? defaultTimeoutSeconds(mode);
  const model = resolveModel(args.modelId);
  const outputImagePath = args.imagePath ? normalizeOutputImagePath(args.imagePath) : null;
  const rawJsonPath = args.rawJsonPath
    ? normalizeJsonPath(args.rawJsonPath)
    : outputImagePath
      ? normalizeJsonPath(defaultRawJsonPath(outputImagePath))
      : null;

  await ensureConsent(args.acceptDisclaimer, args.stageLogs);
  const c = new GeminiClient();
  logStage(args.stageLogs, 'init', `Initializing Gemini client with model=${model.model_name}, mode=${mode}, timeout=${timeoutSeconds}s`);
  await c.init({ verbose: false, timeout: timeoutSeconds });
  try {
    let sess: SessionRecord | null = null;
    let chat = null as any;
    let out: ModelOutput | null = null;
    let selectedImage: SelectedImage | null = null;
    let savedImage: string | null = null;

    if (args.sessionId) {
      sess = (await loadSession(args.sessionId)) ?? {
        id: args.sessionId,
        metadata: [null, null, null],
        messages: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      chat = c.start_chat({ metadata: sess.metadata, model });
    }

    const files = args.referenceImages.length > 0 ? args.referenceImages : null;

    logStage(
      args.stageLogs,
      'submit',
      `Submitting ${mode} request${files ? ` with ${files.length} reference image(s)` : ''}${args.sessionId ? ` in session ${args.sessionId}` : ''}`,
    );

    try {
      if (chat) out = await chat.send_message(effectivePrompt, files);
      else out = await c.generate_content(effectivePrompt, files, model);

      logStage(args.stageLogs, 'response', `Received ${out.candidates.length} candidate(s) and ${out.images.length} image(s)`);
      selectedImage = selectOutputImage(out);

      if (rawJsonPath) {
        await writeResponseDebugJson(rawJsonPath, out, {
          savedImage: null,
          savedRawJson: rawJsonPath,
          selectedImageCandidate: selectedImage?.candidateIndex ?? null,
          selectedImageIndex: selectedImage?.imageIndex ?? null,
          sessionId: args.sessionId,
          model: model.model_name,
          mode,
          originalPrompt: prompt,
          effectivePrompt,
        });
        logStage(args.stageLogs, 'debug', `Saved parsed response JSON to ${rawJsonPath}`);
      }

      if (outputImagePath) {
        const dir = path.dirname(outputImagePath);
        await mkdir(dir, { recursive: true });
        if (!selectedImage) {
          throw new Error(`No image returned in any response candidate. Debug JSON saved to ${rawJsonPath}`);
        }

        const fn = path.basename(outputImagePath);

        logStage(args.stageLogs, 'save', `Downloading image to ${outputImagePath}`);
        if (selectedImage.image instanceof GeneratedImage) {
          savedImage = await selectedImage.image.save(dir, fn, undefined, false, false, true);
        } else {
          savedImage = await selectedImage.image.save(dir, fn, c.cookies, false, false);
        }
        logStage(args.stageLogs, 'save', `Saved image to ${savedImage}`);

        if (rawJsonPath) {
          await writeResponseDebugJson(rawJsonPath, out, {
            savedImage,
            savedRawJson: rawJsonPath,
            selectedImageCandidate: selectedImage.candidateIndex,
            selectedImageIndex: selectedImage.imageIndex,
            sessionId: args.sessionId,
            model: model.model_name,
            mode,
            originalPrompt: prompt,
            effectivePrompt,
          });
        }
      }

      if (sess && args.sessionId) {
        const now = new Date().toISOString();
        sess.updatedAt = now;
        sess.metadata = (chat?.metadata ?? sess.metadata).slice(0, 3);
        sess.messages.push({ role: 'user', content: effectivePrompt, timestamp: now });
        sess.messages.push({ role: 'assistant', content: out.text ?? '', timestamp: now });
        await saveSession(sess);
      }

      if (args.json) {
        console.log(formatJson(out, {
          savedImage,
          savedRawJson: rawJsonPath,
          selectedImageCandidate: selectedImage?.candidateIndex ?? null,
          selectedImageIndex: selectedImage?.imageIndex ?? null,
          sessionId: args.sessionId,
          model: model.model_name,
          mode,
        }));
      } else if (outputImagePath) {
        console.log(savedImage ?? '');
      } else {
        console.log(out.text);
      }
    } catch (error) {
      if (rawJsonPath) {
        try {
          await writeResponseDebugJson(rawJsonPath, out, {
            savedImage,
            savedRawJson: rawJsonPath,
            selectedImageCandidate: selectedImage?.candidateIndex ?? null,
            selectedImageIndex: selectedImage?.imageIndex ?? null,
            sessionId: args.sessionId,
            model: model.model_name,
            mode,
            originalPrompt: prompt,
            effectivePrompt,
            error: error instanceof Error ? error.message : String(error),
          });
          logStage(args.stageLogs, 'debug', `Saved error debug JSON to ${rawJsonPath}`);
        } catch {}
      }
      throw error;
    }
  } finally {
    await c.close();
  }
}

main().catch((e) => {
  const msg = e instanceof Error ? e.message : String(e);
  console.error(msg);
  process.exit(1);
});
