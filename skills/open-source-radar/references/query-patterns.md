# Query Patterns

## Contents

- GitHub Trending
- GitHub Topics
- GitHub Search
- Search shaping rules
- Query examples by domain

## GitHub Trending

Use GitHub Trending to capture recent star momentum:

- `https://github.com/trending?since=daily`
- `https://github.com/trending?since=weekly`
- `https://github.com/trending?since=monthly`

Language-specific trending:

- `https://github.com/trending/python?since=weekly`
- `https://github.com/trending/typescript?since=monthly`

Spoken-language filtering exists for repository trending and is useful when the user wants projects whose descriptions are in Chinese or English.

## GitHub Topics

Use topic pages as domain landing pages:

- `https://github.com/topics/<topic>`

Examples:

- `https://github.com/topics/ai-agents`
- `https://github.com/topics/esp32`
- `https://github.com/topics/quantitative-finance`
- `https://github.com/topics/remotion`

## GitHub Search

Prefer repo search when the user gives a keyword, niche, or stack combination.

Useful qualifiers:

- `topic:<topic>`
- `language:<language>`
- `stars:>N`
- `fork:false`
- `archived:false`
- `pushed:>=YYYY-MM-DD`
- `created:>=YYYY-MM-DD`

Useful sort modes:

- `sort:updated-desc` for current activity
- `sort:stars-desc` for canonical leaders

Build searches that balance recency and credibility. Strong default pattern:

- `topic:<topic> archived:false fork:false pushed:>=<recent-cutoff-date> sort:updated-desc`

Date rule:

- Compute `<recent-cutoff-date>` from the current date and the user's requested window.
- Do not hardcode calendar dates in reusable examples.
- When presenting results, include either the exact query string or the final GitHub search URL.

Search URL pattern:

- `https://github.com/search?q=<url-encoded-query>&type=repositories`

Preference rule:

- In final answers, prefer GitHub search URLs or exact GitHub query strings over generic web-search phrases.
- If generic web discovery queries were needed, label them separately as support rather than as the main reproducibility trail.
- If GitHub web search pages fail, GitHub Search API queries are an acceptable fallback and should be labeled as such.

## Search shaping rules

- Start narrow with exact topic tags or exact brand names.
- If the result set is weak, widen by:
  - adding aliases
  - dropping language filters
  - searching name, description, and readme text
- If the result set is broad or noisy, extract recurring GitHub topics from the strongest matching repos and rerun focused topic queries.
- For noisy words like `claw`, use exact brand matches first.
- For trend-seeking requests, combine:
  - one search for recent updates
  - one search for stars leaders
  - one trending or topic page

## Query examples by domain

Generic fallback:

- `<keyword> in:name,description,readme archived:false fork:false sort:updated-desc`
- `<keyword> in:name,description,readme archived:false fork:false sort:stars-desc`
- `topic:<candidate-topic> archived:false fork:false pushed:>=<recent-cutoff-date> sort:updated-desc`
- `"<exact brand or product name>" archived:false fork:false sort:updated-desc`

AI Agent:

- `topic:ai-agents archived:false fork:false pushed:>=<recent-cutoff-date> sort:updated-desc`
- `topic:mcp archived:false fork:false sort:updated-desc`
- `agentic-ai archived:false fork:false sort:updated-desc`

ESP32:

- `topic:esp32 archived:false fork:false pushed:>=<recent-cutoff-date> sort:updated-desc`
- `topic:esp-idf archived:false fork:false sort:updated-desc`

OpenClaw:

- `openclaw in:name,description,readme archived:false fork:false sort:updated-desc`
- `openclaw in:name,description,readme sort:stars-desc`

Finance:

- `topic:quantitative-finance archived:false fork:false pushed:>=<recent-cutoff-date> sort:updated-desc`
- `topic:algorithmic-trading archived:false fork:false sort:updated-desc`
- `topic:finance language:Python archived:false fork:false sort:updated-desc`

Video creation:

- `topic:video-generation archived:false fork:false sort:updated-desc`
- `topic:remotion archived:false fork:false sort:updated-desc`
- `topic:video-editing archived:false fork:false sort:updated-desc`

Interesting and inspiring:

- `topic:creative-coding archived:false fork:false sort:updated-desc`
- `topic:generative-art archived:false fork:false sort:updated-desc`
