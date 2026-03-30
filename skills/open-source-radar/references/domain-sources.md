# Domain Sources

These are starter presets, not the boundary of the skill. Use the matching section when a topic clearly fits. If nothing fits well, skip the presets and use the generic fallback in [../SKILL.md](../SKILL.md).

## Contents

- Generic fallback hints
- Preset schema
- AI Agent and MCP
- ESP32 and embedded
- OpenClaw and claw variants
- Finance and markets
- Video creation
- Interesting and inspiring projects

## Generic fallback hints

For an unfamiliar topic:

- derive 2-6 aliases from the user's wording
- check GitHub Trending for the requested window
- search GitHub Topics for exact or near-synonym tags
- run GitHub repo search for recent activity and stars leaders
- when broad keyword search is noisy, harvest repeated topics from the strongest hits and rerun topic-based queries
- identify likely official orgs, release pages, or discussions
- add one ecosystem-specific source only when GitHub alone leaves obvious gaps

Useful generic query terms:

- exact keyword
- singular and plural forms
- obvious abbreviations
- adjacent stack names or protocol names
- official company, org, or framework names

## Preset schema

When adding a new preset, keep the structure consistent:

1. `Aliases`
2. `Primary GitHub pages`
3. `Useful query terms`
4. Optional:
   - `Outside GitHub`
   - `Watch targets`
   - `Cautions`

Each preset should stay short and operational. Prefer starter aliases and fixed entry points over long explanations.

## AI Agent and MCP

Aliases:

- `ai agent`, `ai agents`, `agentic ai`, `mcp`, `code agent`

Primary GitHub pages:

- `https://github.com/trending?since=daily`
- `https://github.com/trending?since=weekly`
- `https://github.com/trending?since=monthly`
- `https://github.com/topics/ai-agent`
- `https://github.com/topics/ai-agents`
- `https://github.com/topics/agentic-ai`
- `https://github.com/topics/mcp`

Useful query terms:

- `agent`, `agents`, `ai-agent`, `multi-agent`, `agentic-ai`, `mcp`, `code agent`, `swe agent`

Outside GitHub:

- Hugging Face trending for models or demos when the request is broader than repos.
- Use official project docs or releases when the user asks about one specific framework.

## ESP32 and embedded

Aliases:

- `esp32`, `esp-idf`, `arduino esp32`, `embedded systems`

Primary GitHub pages:

- `https://github.com/topics/esp32`
- `https://github.com/topics/esp-idf`
- `https://github.com/topics/embedded-systems`
- `https://github.com/espressif`

Useful query terms:

- `esp32`, `esp-idf`, `arduino-esp32`, `embedded`, `idf component`, `micropython esp32`

Watch targets:

- Espressif org pages, core SDK repos, and release feeds often matter more than raw stars.

## OpenClaw and claw variants

Aliases:

- `openclaw`, `claw runtime`, `claw agent`

Primary GitHub pages:

- `https://github.com/openclaw/openclaw`
- `https://github.com/openclaw/openclaw/releases`
- `https://github.com/openclaw/openclaw/discussions`
- GitHub search results for exact `openclaw`

Useful query terms:

- `openclaw`, `claw runtime`, `claw agent`, `openclaw plugin`, `openclaw skill`

Cautions:

- Start with exact `openclaw` matches.
- Expand into `mcp`, `agentic-ai`, `sandbox`, `memory`, and `context` ecosystem terms only when exact matches are sparse.
- Do not treat generic "claw" results as relevant without checking the description.

## Finance and markets

Aliases:

- `finance`, `quant`, `quantitative finance`, `algorithmic trading`

Primary GitHub pages:

- `https://github.com/topics/finance`
- `https://github.com/topics/quant`
- `https://github.com/topics/quantitative-finance`
- `https://github.com/topics/algorithmic-trading`
- `https://github.com/topics/trading-bot`

Useful query terms:

- `finance`, `quant`, `algorithmic trading`, `backtesting`, `market data`, `portfolio`, `options`, `trading agent`

Cautions:

- Separate tools into data, research, backtesting, live trading, and AI-for-finance when useful.
- Popularity is not evidence of strategy quality.

## Video creation

Aliases:

- `video creation`, `video generation`, `video editing`, `remotion`

Primary GitHub pages:

- `https://github.com/topics/video-generation`
- `https://github.com/topics/video-editing`
- `https://github.com/topics/remotion`
- `https://github.com/remotion-dev`

Useful query terms:

- `video generation`, `video editing`, `remotion`, `ffmpeg`, `motion graphics`, `comfyui video`

Outside GitHub:

- Hugging Face Spaces or models trending is useful for AI video tooling and demos.

## Interesting and inspiring projects

Aliases:

- `interesting`, `inspiring`, `creative coding`, `generative art`

Primary GitHub pages:

- `https://github.com/trending?since=weekly`
- `https://github.com/trending?since=monthly`
- `https://github.com/collections`
- `https://github.com/topics/creative-coding`
- `https://github.com/topics/generative-art`

Useful query terms:

- `creative coding`, `generative art`, `toy project`, `weird`, `demo`, `showcase`

Outside GitHub:

- Hacker News `Show HN` is useful for polished, surprising, or early-stage projects that may not yet have large star counts.
