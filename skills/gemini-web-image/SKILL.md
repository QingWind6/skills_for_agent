---
name: gemini-web-image
description: Generate or vary a single image through Gemini Web using a dedicated local Chrome profile and cached cookies instead of the official API. Use only when the user explicitly wants Gemini web image generation; text mode exists only for diagnostics.
version: 0.1.0
metadata:
  openclaw:
    homepage: local
    requires:
      anyBins:
        - bun
        - npx
---

# Gemini Web Image

Pure web-based Gemini image generation via reverse-engineered browser login. This skill is image-first. Text mode is only for diagnostics and smoke tests.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `{baseDir}`
2. Script path = `{baseDir}/scripts/<script-name>.ts`
3. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun
4. Replace all `{baseDir}` and `${BUN_X}` in this document with actual values

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for image generation |
| `scripts/gemini-webapi/*` | TypeScript port of `gemini_webapi` (GeminiClient, types, utils) |

## Consent Check (REQUIRED)

Before first use, verify user consent for reverse-engineered API usage.

**Consent file locations**:
- macOS: `~/Library/Application Support/gemini-web-image/data/consent.json`
- Linux: `~/.local/share/gemini-web-image/data/consent.json`
- Windows: `%APPDATA%\gemini-web-image\data\consent.json`

**Flow**:
1. Check if consent file exists with `accepted: true` and `disclaimerVersion: "1.0"`
2. If valid consent exists → print warning with `acceptedAt` date, proceed
3. If no consent:
   - Ask the user explicitly in chat before running the skill, or
   - run the CLI in a TTY and accept interactively, or
   - pass `--accept-disclaimer` for an explicit non-interactive first run
4. Consent file format: `{"version":1,"accepted":true,"acceptedAt":"<ISO>","disclaimerVersion":"1.0"}`

## Usage

```bash
# Image generation
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cute cat" --image cat.png
${BUN_X} {baseDir}/scripts/main.ts --mode image --prompt "A cute cat" --image cat.png
${BUN_X} {baseDir}/scripts/main.ts --promptfiles system.md content.md --image out.png
${BUN_X} {baseDir}/scripts/main.ts --prompt "A cute cat" --image cat.png --raw-json cat.response.json

# Reference-image variation
${BUN_X} {baseDir}/scripts/main.ts --prompt "Create variation" --reference a.png --image out.png

# Dedicated profile login
${BUN_X} {baseDir}/scripts/main.ts --login
${BUN_X} {baseDir}/scripts/main.ts --login --accept-disclaimer

# Text diagnostics only
${BUN_X} {baseDir}/scripts/main.ts --mode text --prompt "Hello" --json
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt`, `-p` | Prompt text |
| `--promptfiles` | Read prompt from files (concatenated) |
| `--model`, `-m` | Model: gemini-3-pro (default), gemini-3-flash, gemini-3-flash-thinking, gemini-3.1-pro-preview |
| `--mode <kind>` | `auto`, `text`, or `image`. `--image` implies image mode. |
| `--image [path]` | Output image path. This flag switches the request into image mode. |
| `--raw-json <path>` | Save parsed response JSON for debugging. Defaults to `<image>.response.json`. |
| `--reference`, `--ref` | Reference images for variation or image-conditioned requests |
| `--sessionId` | Session ID for advanced multi-turn diagnostics |
| `--list-sessions` | List saved sessions |
| `--json` | Output as JSON |
| `--login` | Refresh cookies, then exit |
| `--accept-disclaimer` | Record consent non-interactively for first use |
| `--cookie-path` | Custom cookie file path |
| `--profile-dir` | Chrome profile directory |
| `--timeout <seconds>` | Override request timeout |
| `--no-auto-image-prompt` | Disable automatic image-only prompt wrapper |
| `--quiet-stages` | Suppress stderr stage logs |

## Models

| Model | Description |
|-------|-------------|
| `gemini-3-pro` | Default, latest 3.0 Pro |
| `gemini-3-flash` | Fast, lightweight 3.0 Flash |
| `gemini-3-flash-thinking` | 3.0 Flash with thinking |
| `gemini-3.1-pro-preview` | 3.1 Pro preview (empty header, auto-routed) |

## Authentication

First run opens a dedicated Chrome profile for Google and Gemini Web login. Complete Google sign-in and any Gemini onboarding in that browser window. Cookies are cached automatically.

This skill stores its own state only in the `gemini-web-image` namespace:
- cookie cache and consent under `gemini-web-image/data`
- dedicated Chrome profile under `gemini-web-image/chrome-profile`
- chat sessions under `gemini-web-image/data/sessions`

It does not reuse legacy `baoyu-skills/gemini-web` cookies or profile directories.

Supported browsers (auto-detected): Chrome, Chrome Canary/Beta, Chromium, Edge.

Force refresh: `--login` flag. Override browser: `GEMINI_WEB_CHROME_PATH` env var.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_WEB_DATA_DIR` | Data directory |
| `GEMINI_WEB_COOKIE_PATH` | Cookie file path |
| `GEMINI_WEB_CHROME_PROFILE_DIR` | Chrome profile directory |
| `GEMINI_WEB_CHROME_PATH` | Chrome executable path |
| `GEMINI_WEB_ACCEPT_DISCLAIMER` | Set to `1` or `true` to pre-accept the disclaimer |
| `HTTP_PROXY`, `HTTPS_PROXY` | Proxy for Google access (set inline with command) |

## Sessions

Session files stored in data directory under `sessions/<id>.json`.

Contains: `id`, `metadata` (Gemini chat state), `messages` array, timestamps.

## Upgrade Notes

- `--image` is treated as a real image mode, not just a save path hint.
- Image mode auto-injects an explicit "generate one image" wrapper unless `--no-auto-image-prompt` is used.
- When `--image` is used, the parsed response is also saved to `<image>.response.json` by default, including error details when generation fails after request submission.
- Stage logs are printed to stderr for `init`, `submit`, `response`, `debug`, and `save` unless `--quiet-stages` is used.
- If Gemini returns multiple candidates, the first candidate containing an image is selected for saving.
- Profile and cookie state are fully isolated to this skill's own namespace.
