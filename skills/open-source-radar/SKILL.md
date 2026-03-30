---
name: open-source-radar
description: Find and summarize current open-source trends for any domain, niche, technology, or keyword by using live GitHub and adjacent ecosystem sources. Use when Codex needs to identify hot, fast-rising, or worth-following projects; compare daily, weekly, and monthly momentum; or build a compact radar from a user-supplied topic. Treat domain presets as optional accelerators, not as the skill boundary.
---

# Open Source Radar

Track a topic as a repeatable radar workflow: normalize the user's keyword, choose the right live sources, gather candidates from trending, topics, search, and release activity, then return a short list with a trend summary and follow targets. Use domain presets when they help, but always support unknown or brand-new topics through the generic fallback flow.

## Quick Start

1. Normalize the request into:
   - topic or niche
   - time window: daily, weekly, monthly, or rolling recent
   - intent: hot now, trend direction, worth following, or inspiration scan
2. Resolve any date cutoffs relative to the current date. Never hardcode example dates into live queries.
3. Use live sources. Do not answer from memory for trend status.
4. Pull candidates from at least:
   - one trending-style source
   - one topic or category source
   - one search or release-activity source
5. Record the exact query strings or query URLs as you search so the result is reproducible.
6. Rank candidates by recent momentum, current maintenance, ecosystem relevance, and novelty.
7. Return:
    - the exact time basis with an absolute date
    - 5-12 recommended projects
    - 2-5 trend directions
    - 3-6 repos, orgs, or pages worth watching
    - the exact queries or search URLs used
    - any important source gaps or failures
8. Link every live source used.
9. Use plain Markdown links only. Do not emit tool-specific citation placeholders, internal reference tokens, or testing meta text.

Source priority:

1. GitHub official pages: trending, topics, repo, releases, tags, org pages, discussions
2. Official project sites or docs
3. Ecosystem-specific platforms
4. Third-party write-ups only as supporting context

## Interpret the request

Map loose user wording into a stable intent before searching:

- `最近有什么火的`, `热门`, `榜单`, `这周/月有什么新的` -> `Hot now`
- `值得关注`, `值得长期跟`, `未来可能会起来` -> `Worth following`
- `先帮我了解这个方向`, `这个领域现在什么情况` -> `Hot now` plus `Canonical`
- `有趣的`, `有灵感的`, `惊艳的` -> `Interesting` or `inspiring`
- `给我日榜/周榜/月榜` -> exact requested time window
- `帮我持续跟踪` -> answer normally, then also include `Watch targets`
- `what's hot`, `trending`, `what's new recently` -> `Hot now`
- `what should I watch`, `worth following`, `what matters next` -> `Worth following`
- `show me cool stuff`, `interesting`, `inspiring` -> `Interesting` or `inspiring`
- `daily`, `weekly`, `monthly` -> exact requested time window

Default behavior when the wording is broad:

- use `weekly` for "what is happening recently"
- use `monthly` for "trend direction"
- include both `Hot now` and `Worth following` unless the user clearly wants only one

## Generic Fallback

Use this when the topic does not clearly match a preset in [references/domain-sources.md](references/domain-sources.md):

1. Search GitHub Trending for the relevant time window.
2. Search GitHub Topics for exact and near-synonym tags.
3. Run GitHub repository search for:
   - exact keyword match
   - alias or synonym matches
   - recent activity with `pushed:>=... sort:updated-desc`
   - canonical leaders with `sort:stars-desc`
4. If the broad keyword is noisy, extract candidate GitHub topics from the strongest hits and rerun more focused topic searches.
5. Check likely official orgs, release pages, or discussions for the most credible hits.
6. If the area is tool or model adjacent, add one ecosystem-specific source only when it improves coverage.

Do not let third-party news or launch write-ups become the primary evidence for a project's relevance when GitHub repo, release, or official pages are available.

## Failure Handling

When a preferred source is unavailable, sparse, or obviously noisy:

1. State which source failed, was blocked, or returned weak results.
2. Fall back in this order:
   - another GitHub official page
   - GitHub repository search
   - GitHub Search API when the web UI is blocked or unstable
   - official org, release, or discussion pages
   - one ecosystem-specific source
3. Keep the result narrow rather than padding with weak matches.
4. Add a short `Source gaps` note in the answer when failures materially reduce confidence.
5. If live sources are unavailable entirely, say that current trend status could not be verified and stop short of trend claims.

## Workflow

### 1. Normalize the topic

- Expand common aliases before searching. Presets are examples, not a closed list:
  - `AI Agent` -> `ai-agent`, `ai-agents`, `agentic-ai`, `mcp`
  - `OpenClaw`, `claw`, `龙虾 claw` -> `openclaw` plus nearby agent runtime and MCP ecosystem terms
  - `股票金融市场` -> `finance`, `quant`, `quantitative-finance`, `algorithmic-trading`
  - `视频创作` -> `video-generation`, `video-editing`, `remotion`, `creative tools`
- If the user gives only one short keyword, infer a small alias set and clearly say when that mapping is an inference.
- If a nickname is noisy, start with exact matches, then widen to adjacent ecosystem tags only when needed.
- If no known preset matches, keep going with the generic fallback instead of asking for a narrower topic unless ambiguity is severe.
- Resolve rolling cutoffs such as `last 30 days` or `recent` from the current date, and prefer placeholder logic like `<recent-cutoff-date>` in examples rather than fixed calendar dates.

### 2. Pick the source stack

- Start with GitHub official sources.
- Then load the matching preset entry points from [references/domain-sources.md](references/domain-sources.md), if one exists.
- Use [references/query-patterns.md](references/query-patterns.md) for GitHub search syntax and query shaping.
- Use [references/signal-checklist.md](references/signal-checklist.md) to separate "hot now" from "worth following."
- If no preset exists, rely on the generic fallback and create a small alias set from the user's wording.

### 3. Gather candidates

- Prefer 3 channels at minimum:
  - trending
  - topic or category
  - search, releases, or discussions
- Preserve the exact search query or URL for every important candidate-gathering step.
- Prefer GitHub search URLs, topic pages, repo pages, and release pages over generic web-search queries in the final answer.
- When the direction is niche, accept lower absolute stars if update activity and ecosystem fit are strong.
- When the user wants to "与时俱进", bias toward projects with strong movement in the last 30-90 days rather than all-time star leaders.

### 4. Rank and trim

- Prefer projects that satisfy most of:
  - strong recent star gain or trending placement
  - active commits or recent release
  - clear description and real usage
  - relevant ecosystem fit for the target topic
  - evidence of surrounding adoption, plugins, forks, or discussions
- Down-rank:
  - abandoned star giants
  - empty wrappers with weak docs
  - generic `awesome-*` indexes unless the user explicitly wants curation
  - unrelated `claw` matches when the topic is OpenClaw
- For `interesting` or `inspiring` requests, novelty and taste can outrank raw stars.

### 5. Produce the answer

- Include the exact time basis such as `As of <current-date>` or `GitHub daily trending on <current-date>`.
- Use the actual current date and resolved time window. Do not reuse example dates from the skill text.
- Separate:
  - `Hot now`
  - `Worth following`
  - `Watch list`
  - `Trend directions`
- State when a theme is not a GitHub official category and is instead an inferred grouping from topic tags, repo descriptions, release activity, and adjacent ecosystem pages.
- For finance-related topics, explicitly avoid treating project popularity as investment advice or market signal quality.
- Follow the templates in [references/output-templates.md](references/output-templates.md).
- Start with a plain one-line scope statement. Do not render it as `Scope`, `## Scope`, or any other heading.
- Always include reproducibility details:
  - exact query strings, search URLs, or topic pages
  - source failures or thin-signal notes when relevant
- When a project is named, prefer linking its GitHub repo or release page directly. Use third-party coverage only as support.
- Keep the section titles stable. Do not rename `Watch targets`, `Queries used`, `Source gaps`, or `Sources`.
- Do not add meta lines such as `Testing not run`.
- Do not output internal citation artifacts such as tool trace markers or unresolved reference tokens.

## Domain Notes

- Read [references/domain-sources.md](references/domain-sources.md) for optional presets, starter aliases, and fixed entry points.
- Read [references/query-patterns.md](references/query-patterns.md) when building GitHub searches from the user's keywords.
- Read [references/signal-checklist.md](references/signal-checklist.md) when deciding what to surface and how to present it.
- When adding new presets, follow the preset schema in [references/domain-sources.md](references/domain-sources.md) instead of inventing a new section shape.

## Output Pattern

Use a compact structure unless the user asks for depth. Default order:

- one-line scope statement with date and source set
- `Hot now`
- `Worth following`
- `Watch list`
- short list of trend directions
- short list of repos, orgs, or pages to watch
- `Queries used`
- `Source gaps`
- `Sources`

If the result set is thin:

- say that the topic is niche or noisy
- keep the best 3-6 repos only
- explain what made them the strongest available signals
- avoid padding with weak matches

Formatting rules for final outputs:

- Write the scope as a plain sentence or single line before the main sections, not as a Markdown heading.
- `Queries used` should prefer exact GitHub URLs, GitHub topic pages, GitHub API URLs, or exact repository-search query strings.
- If generic web discovery phrases were used during exploration, do not let them dominate the final `Queries used` list.
- `Sources` must contain readable source names plus plain links, not raw trace tokens or empty bullets.
- If there are no meaningful source gaps, say `No major source gaps.` instead of `None`.

## Resources

- [references/domain-sources.md](references/domain-sources.md): domain-by-domain source map, alias hints, and fixed pages to check
- [references/query-patterns.md](references/query-patterns.md): GitHub topic, trending, and search query patterns
- [references/signal-checklist.md](references/signal-checklist.md): ranking rules, weak-signal filters, and answer shape
- [references/output-templates.md](references/output-templates.md): stable answer structures for radar scans, trend checks, and inspiration scans
