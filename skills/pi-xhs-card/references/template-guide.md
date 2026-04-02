# Template Guide

## Built-In Templates

### `editorial-tech`

- Best for: AI tools, open-source radar, market scans, trend commentary
- Personality: serif headline, editorial cover, soft geometric accents
- Strength: strong hero titles and report-like tone

### `knowledge-clean`

- Best for: tutorials, lists, framework comparisons, tool recommendations
- Personality: gridded, minimal, structured, calm
- Strength: clean scanning and predictable information hierarchy

### `study-notes`

- Best for: methods, study plans, reading notes, lighter creator voice
- Personality: notebook cues, dashed borders, warmer tone
- Strength: more casual and friendly than the other two templates

## How To Add A Template

1. Add the template object to `TEMPLATES` in `public/app.js`.
2. Add picker swatch styles under `.theme-<template-id>` in `public/styles.css`.
3. Add card styles under `.template-<template-id>` in `public/styles.css`.
4. Set `meta.templateId` in `deck.json` to test the new template.
5. Run the studio, export once, and confirm there are no layout issues.

Rules:

- Keep template ids kebab-case.
- Match picker preview and actual card styles so the selector is truthful.
- Preserve export safety. New templates must still work with the overflow blocker.

## Files To Touch

- `public/app.js`: template metadata and render registration
- `public/styles.css`: picker swatches, shell accents, and card visuals
- `deck.json`: default testing template for the current brief
