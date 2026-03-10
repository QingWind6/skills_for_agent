# skills_for_agent

A curated repository of reusable agent skills, references, and helper scripts.

This repo is designed to store portable skill folders that can be copied into a compatible agent runtime, or adapted for other agent systems such as Codex, Claude-oriented wrappers, OpenClaw, and similar tool-using assistants.

## Repository Layout

```text
skills_for_agent/
├── README.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── agents/
│       ├── scripts/
│       ├── references/
│       └── assets/
└── *.md
```

- `skills/`: primary home for reusable skill folders
- `SKILL.md`: core instructions and trigger metadata for a skill
- `agents/`: optional agent-specific metadata such as `openai.yaml`
- `scripts/`: helper utilities the skill can run directly
- `references/`: deeper docs loaded only when needed
- root-level `*.md`: standalone guides or legacy references that are not yet packaged as full skills

## Installation

### Codex / Codex CLI

Copy a skill folder into `~/.codex/skills/`:

```bash
mkdir -p ~/.codex/skills
cp -R skills/imgui-repo-navigator ~/.codex/skills/
```

### Generic installation flow

For other agent frameworks, keep the skill folder intact and install it into that agent's skill/plugin directory, or point the agent at the folder directly if supported.

Minimum portable unit:

- the entire skill folder
- `SKILL.md`
- any referenced `scripts/` and `references/`

### Dependencies

Each skill may declare its own runtime requirements. For example:

- `skills/imgui-repo-navigator` requires `python3`
- upstream GitHub fallback also requires network access

## Skills Index

| Skill | Purpose | Key Dependencies | Notes |
|---|---|---|---|
| `imgui-repo-navigator` | Find Dear ImGui APIs, examples, backend files, and docs from a local checkout or upstream GitHub | `python3`, optional network | Local-first, GitHub fallback |
| `n8n-api-v1` | Operate n8n API v1 with authenticated request patterns and endpoint references | n8n API access, optional `curl`/`jq` | Defaults to local `localhost:5678/api/v1`, base URL overridable |
| `project-continuity-manager` | Keep large projects coherent across many sessions and agents with a durable `docs/agent/` memory layer and validated handoffs | `python3`, optional `git` | Initializes templates, checks docs health, creates handoffs, validates handoffs, and checks handoff freshness |

## Skill Packaging Guidelines

Recommended rules for new skills added to this repo:

1. Keep each skill self-contained in its own folder under `skills/`
2. Put trigger logic and operating instructions in `SKILL.md`
3. Put long reference material in `references/`
4. Put executable helpers in `scripts/`
5. Keep agent-specific metadata optional and non-blocking
6. Prefer cross-platform scripts when possible
7. Prefer local/project-aware lookup first, then upstream/network fallback when that improves portability

## Example Usage

Use the ImGui skill after installation:

```text
Use $imgui-repo-navigator to find the correct Win32 + DX9 backend integration flow.
```

Or run its helper directly:

```bash
python skills/imgui-repo-navigator/scripts/find_imgui_targets.py win32 dx9
python skills/imgui-repo-navigator/scripts/find_imgui_targets.py --mode upstream --ref master docking
```
