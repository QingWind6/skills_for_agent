---
name: pi-xhs-card
description: Create, edit, preview, and export Xiaohongshu (小红书 / XHS) card decks as template-driven web pages with live preview and PNG output. Use when Codex needs to generate or revise multi-card Xiaohongshu posts, bootstrap a local card studio, edit `deck.json`, add or tune visual templates, fix cropped exports, or ship a browser-based workflow for browsing, editing, and exporting XHS cards.
---

# PI XHS Card

Build Xiaohongshu cards as DOM and CSS, not hand-drawn bitmaps. Keep `deck.json` as the single source of truth, use the local studio for editing and preview, and export only after the built-in overflow checker reports no layout issues.

## Quick Start

1. Pick a target studio directory. If the user does not provide one, default to `./pi-xhs-card-studio`.
2. Bootstrap the starter with [`scripts/init-studio.sh`](scripts/init-studio.sh) `<target-dir>`.
3. Read [`references/deck-schema.md`](references/deck-schema.md) before editing `deck.json`.
4. Fill `deck.json` from the user's brief.
5. Run [`scripts/validate-studio.sh`](scripts/validate-studio.sh) `<target-dir>`.
6. Start the studio with `node <target-dir>/server.mjs`. If binding `127.0.0.1` fails inside the sandbox, rerun with escalated permissions.
7. Open the page in a browser, or export via [`scripts/export-studio.sh`](scripts/export-studio.sh) `<base-url>`.
8. If export is blocked, shorten copy, split the content across more cards, or switch template before retrying.

## Workflow

### Translate the brief into a deck

- Default to five cards unless the user asks for a different structure:
  - `cover`
  - one or two `ranking` cards
  - one `insight` card
  - one `closing` card
- Keep copy short and decisive. Let the overflow checker be the final arbiter.
- Prefer Chinese body copy, but keep repository names, product names, and stats in their original form.
- Keep card order intentional because `deck.json` order is also preview and export order.

### Pick the template

- Read [`references/template-guide.md`](references/template-guide.md) when choosing or extending templates.
- Use `editorial-tech` for AI, open-source, report, and trend-watch content.
- Use `knowledge-clean` for lists, tutorials, tool recommendations, and structured knowledge cards.
- Use `study-notes` for reading notes, study plans, or lighter creator tone.
- When adding a template, update both `public/app.js` and `public/styles.css`. Do not add a template in only one file.

### Keep exports safe

- The studio exports fixed `1080x1440` PNG cards.
- The browser sets `window.__LAYOUT_ISSUES__` and blocks export when any card overflows.
- Fix clipped exports by reducing copy density, splitting a card, or choosing a more spacious template. Do not bypass the overflow check.

### Edit the correct files

- Content, ordering, and template choice live in `deck.json`.
- Template metadata and per-card render logic live in `public/app.js`.
- Visual language lives in `public/styles.css`.
- Local API and file persistence live in `server.mjs`.
- Headless export lives in `export.mjs`.

## Resources

- [`assets/studio-template/`](assets/studio-template/): portable starter with the current editor, preview, export flow, and sample deck.
- [`references/deck-schema.md`](references/deck-schema.md): card types, fields, and editing rules.
- [`references/template-guide.md`](references/template-guide.md): template chooser and extension notes.
- [`scripts/init-studio.sh`](scripts/init-studio.sh): copy the bundled studio into a target folder.
- [`scripts/validate-studio.sh`](scripts/validate-studio.sh): run the core syntax checks.
- [`scripts/export-studio.sh`](scripts/export-studio.sh): trigger PNG export from a running studio.
