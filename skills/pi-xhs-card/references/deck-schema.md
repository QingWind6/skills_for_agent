# Deck Schema

Use `deck.json` as the single source of truth for content, order, and template selection.

## Top Level Shape

```json
{
  "meta": {
    "title": "GitHub 热门仓库速览",
    "subtitle": "今日 Top5 + 本周 Top5",
    "templateId": "editorial-tech",
    "aspectRatio": "3:4",
    "updatedAt": "2026-04-01T10:10:16.770Z"
  },
  "cards": []
}
```

Rules:

- Keep `templateId` in sync with a template defined in `public/app.js`.
- Keep `aspectRatio` as `3:4` unless the studio is explicitly redesigned.
- Treat `updatedAt` as runtime-managed metadata.
- Export order follows array order in `cards`.

## Card Types

### `cover`

Fields:

- `id`
- `type`
- `eyebrow`
- `title`
- `subtitle`
- `tags`: string array
- `note`

Use for the first card only unless the user explicitly wants multiple cover-like breaks.

### `ranking`

Fields:

- `id`
- `type`
- `eyebrow`
- `title`
- `rows`: array of `{ "title", "subtitle", "stat" }`
- `note`

Use for leaderboards, lists, comparisons, and tool roundups.

### `insight`

Fields:

- `id`
- `type`
- `eyebrow`
- `title`
- `blocks`: array of `{ "index", "title", "body" }`
- `highlightTitle`
- `highlightBody`

Use for trend summaries, takeaways, and interpretation after the factual list cards.

### `closing`

Fields:

- `id`
- `type`
- `eyebrow`
- `title`
- `groups`: array of `{ "label", "value" }`
- `footer`
- `stamp`

Use for watchlists, next actions, or source notes.

## Editing Rules

- Keep `id` values stable because they are also used as export filenames.
- Prefer 3 to 5 rows in `ranking`, 3 insight blocks in `insight`, and 4 to 6 groups in `closing`.
- When text density grows, split the content into another card instead of shrinking typography.
- If editing through the browser UI, multiline list fields use `|` separators per line. If editing raw JSON, keep the arrays structured.
