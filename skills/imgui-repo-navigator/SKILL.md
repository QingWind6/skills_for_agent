---
name: imgui-repo-navigator
description: Navigate and extract authoritative information from a local Dear ImGui checkout or, when the local repo is missing or does not answer the query, from the official GitHub repository. Use when implementing, modifying, reviewing, or debugging Dear ImGui code; locating public APIs, backend interfaces, official examples, integration order, platform/renderer pairings, fonts, textures, input handling, docking/layout patterns, or build/run instructions for Dear ImGui-based code.
---

# ImGui Repo Navigator

Use local Dear ImGui sources first to stay aligned with the checked-out version. If the local repo is missing or local lookup produces no useful match for the query, fall back to the official upstream GitHub repository.

## Quick Start

1. Run `python scripts/find_imgui_targets.py [terms...]` in `auto` mode.
2. Use `--mode local` when the answer must match the vendored or checked-out version exactly.
3. Use `--mode upstream --ref master|tag|commit` when the task explicitly asks for official upstream behavior or a specific release.
4. Use `--repo PATH` to point at a vendored ImGui subtree inside another project.
5. Use `--github-url URL` only when the upstream is not `https://github.com/ocornut/imgui`.

## Source Priority

1. Explicit `--repo` path.
2. Local workspace repo or vendored subtree containing `imgui.h`, `backends/`, `examples/`, and `docs/`.
3. Official GitHub repo fallback.

In `auto` mode, use local results if they contain a meaningful match. If not, retry against upstream.

## Authority Order

- Treat `imgui.h` as the public API contract.
- Treat backend headers in `backends/` as the public integration contract for a platform or renderer.
- Treat example `main.cpp` files as the reference for init order, per-frame order, shutdown order, and platform glue.
- Treat `imgui_demo.cpp` as the best usage catalog for end-user widgets and patterns.
- Treat `docs/*.md` and `docs/*.txt` as the first stop for conceptual or FAQ-style questions.
- Treat `imgui_internal.h` and internal implementation files as private details; use them only when the task explicitly needs internals or a bug fix.

## Workflow

### Locate the right source

- Start with `scripts/find_imgui_targets.py`.
- Prefer `auto` mode unless the user explicitly asks for local-only or upstream-only behavior.
- When local and upstream may differ, state which source you used and why.

### Classify the task before reading many files

- Core widget or public API question: open `imgui.h`, then `imgui_demo.cpp`, then the matching implementation file.
- Backend or renderer integration question: open the matching `backends/imgui_impl_*.h/.cpp`, then the closest `examples/example_*/main.cpp`.
- Usage or troubleshooting question: open `docs/FAQ.md`, `docs/FONTS.md`, `docs/BACKENDS.md`, or `docs/EXAMPLES.md`.
- Build or run question: open the example `README.md`, `Makefile`, or `CMakeLists.txt`.

### Preserve exactness

- Prefer an exact platform + renderer example.
- If there is no exact example, preserve platform first, renderer second, and state the inference.
- When using upstream fallback, include the GitHub repo and `ref` in the answer.

## Task Rules

### Core API and widgets

- Open `imgui.h` first.
- Open `imgui_demo.cpp` to find working usage patterns.
- Open `imgui_widgets.cpp`, `imgui_tables.cpp`, or `imgui_draw.cpp` only after identifying the relevant API family.

### Backends and integration

- Read the backend header comments and declarations first; they summarize supported features and public entry points.
- Read the backend `.cpp` top section next for implementation notes, changelog items, and platform caveats.
- Read the exact example `main.cpp` that combines the platform backend and renderer backend you need.

### Tool-style desktop UI

- For menu bars, inspect `ImGui::BeginMainMenuBar()` usage in `imgui_demo.cpp` and declarations in `imgui.h`.
- For docking or multi-viewport work, confirm support in the current source before assuming it exists. Search for `DockSpace`, `DockingEnable`, `ViewportsEnable`, and related flags.
- Prefer local demo and example code over ad-hoc internet snippets.

### Fonts, text, textures, and images

- Start with `docs/FONTS.md` and the relevant FAQ entries.
- For image rendering or texture handles, read the FAQ entry about `ImTextureID` and then inspect the active renderer backend header to confirm the expected texture type.

### Build and run

- Use the per-example build files under `examples/`.
- Do not assume a root-level build exists; confirm it from the chosen source.

## Output Expectations

- Reference concrete local file paths when local lookup wins.
- Reference concrete GitHub blob URLs with the chosen `ref` when upstream lookup wins.
- Explain which file is authoritative for the requested fact.
- Call out when you infer from the closest example instead of an exact match.
- State when the answer came from upstream fallback instead of the local checkout.

## Resources

- `references/repo-map.md`: where each class of Dear ImGui information lives.
- `references/example-matrix.md`: platform/renderer example directory map.
- `references/task-playbook.md`: common lookup recipes and lookup mode guidance.
- `scripts/find_imgui_targets.py`: primary cross-platform lookup script.
- `scripts/find_imgui_targets.sh`: shell wrapper that calls the Python script.
