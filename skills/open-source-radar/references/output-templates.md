# Output Templates

## Contents

- Default radar scan
- Short trend check
- Inspiration scan
- Thin-result fallback

## Default radar scan

Use this for most requests:

1. Scope line
   - one plain line, not a `Scope` heading
   - include topic, time window, exact date, and source set
2. Hot now
   - 3-6 repos
   - one line each: what it is and why it is hot now
3. Worth following
   - 2-5 repos
   - one line each: why it looks durable
4. Watch list
   - 2-4 repos
   - one line each: why it is early but notable
5. Trend directions
   - 2-5 bullets
6. Watch targets
   - repos, orgs, topic pages, or release pages
7. Queries used
   - exact GitHub search queries, search URLs, topic pages, or release pages
8. Source gaps
   - failed, blocked, or sparse sources when relevant
9. Sources
   - list every page or source family used

Prefer first-party GitHub and official project links here. Add third-party coverage only as supporting context.
Keep the section names exactly as written above.

## Short trend check

Use this when the user wants a fast answer:

- one-line scope
- `Hot now`: 3-5 repos
- `Trend directions`: 2-3 bullets
- `Watch targets`: 2-4 links
- `Queries used`
- `Source gaps`
- `Sources`

## Inspiration scan

Use this for `有趣的`, `有灵感的`, `惊艳的`, or `show me cool stuff`:

1. Scope line
2. Most interesting
3. Most polished
4. Most novel
5. Themes to explore next
6. Queries used
7. Source gaps
8. Sources

Raw star count matters less here than originality, execution, and recency.

## Thin-result fallback

Use this when the topic is niche, ambiguous, or sparse:

1. Scope line
2. Brief note that the signal is thin, noisy, or early
3. Best available matches
4. What to watch next
5. Queries used
6. Source gaps
7. Sources

Do not pad the list with weak or irrelevant repos just to fill buckets.

## Hygiene rules

- Render the scope as one plain line before the main sections, not as `Scope` or `## Scope`.
- Render links as plain Markdown links, not tool-specific citation placeholders.
- Do not end with testing meta such as `Testing not run`.
- If `Source gaps` is empty, write `No major source gaps.`
- In `Queries used`, prefer exact GitHub URLs or query strings over generic web-search phrases.
