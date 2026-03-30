# Signal Checklist

## Contents

- Classify the request
- Strong signals
- Weak signals
- Ranking buckets
- Answer template

## Classify the request

Treat these as different jobs:

- `Hot now`: what is spiking or newly hot in the chosen window
- `Worth following`: what is likely to matter over the next few months
- `Canonical`: what is foundational or widely adopted
- `Interesting` or `inspiring`: what is surprising, polished, or creatively fresh

## Strong signals

- Appears on GitHub Trending in the relevant window
- Appears repeatedly across topic pages, search results, and surrounding discussions
- Has recent commits or a recent release
- Has a clear demo, docs, or real usage story
- Sits in the right ecosystem at the right time, not just as an old star giant
- Has visible plugin, fork, or community activity when the area is ecosystem-driven

## Weak signals

- Large all-time stars but no current activity
- Thin wrapper repos with little original substance
- Generic `awesome-*` lists when the user wants active projects
- Brand-name collisions, especially with short or noisy terms such as `claw`
- Finance projects with hype but unclear data quality, backtesting method, or maintenance
- Momentum claims supported only by third-party write-ups when first-party repo or release evidence is available

## Ranking buckets

Use these buckets when useful:

- `Hot now`: strong recent movement, currently visible
- `Worth following`: slightly less explosive, but strong maintenance and trajectory
- `Watch list`: early or niche projects that may matter soon

For inspiration-heavy requests, use:

- `Most interesting`
- `Most polished`
- `Most novel`

## Answer template

Use a compact output unless the user asks for depth:

1. Scope line with exact date and source set
2. `Hot now` list with one-line why per repo
3. `Worth following` list with one-line why per repo
4. `Watch list` for early or niche candidates
5. `Trend directions` with 2-5 bullets
6. `Watch targets` with repos, orgs, topic pages, or release pages
7. `Queries used`
8. `Source gaps`
9. `Sources`

Always include links. Always distinguish observed facts from inferred trend judgments.
Keep the exact section names above so outputs stay machine-comparable across tests.
Write the scope as a plain line before the main sections, not as `Scope` or `## Scope`.

## Bucket assignment rules

Put a repo into `Hot now` when it has clear recent visibility, such as trending placement, strong recent star velocity, repeated appearance across sources, or a very recent release that is drawing attention.

Put a repo into `Worth following` when the growth is less explosive but the maintenance, ecosystem fit, and trajectory look durable.

Put a repo into `Watch list` when it is early, niche, or still forming, but has enough current signal that the user should keep an eye on it.

## Source failures and uncertainty

- If a preferred source fails, say so briefly.
- If the signal is thin or noisy, narrow the output instead of broadening with weak matches.
- If trend confidence depends on inference rather than repeated source confirmation, say that explicitly.
- If there are no meaningful source gaps, write `No major source gaps.` rather than leaving an empty or ambiguous section.

## Evidence hierarchy

Prefer evidence in this order:

1. GitHub repo, releases, tags, discussions, org pages, and topic pages
2. Official project docs or homepage
3. Ecosystem-specific source pages
4. Third-party coverage

Use lower-priority sources mainly to add context, not to substitute for first-party evidence when first-party evidence exists.

## Output hygiene

- Use plain Markdown links.
- Do not emit internal tool citation markers, trace tokens, or placeholder references.
- Do not append testing-status notes or other meta commentary unrelated to the user's request.
