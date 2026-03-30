# GitHub List Spec Format

Use a JSON file that is either:

- an array of list objects, or
- an object with a top-level `lists` array

Each entry supports these fields:

- `name`: Final GitHub List name. Required.
- `file`: Text filename inside `--lists-dir`. Required.
- `description`: GitHub List description. Optional but recommended.
- `visibility`: `"public"` or `"private"`. Optional. Defaults to `"public"`.
- `reuse_from`: Existing GitHub List name to rename and reuse when the target List does not already exist. Optional.

## Example

```json
[
  {
    "name": "Embedded / ESP32 / IoT",
    "file": "Embedded-ESP32-IoT.txt",
    "description": "ESP32, embedded systems, Home Assistant, TinyML, and device tooling.",
    "visibility": "public",
    "reuse_from": "Embedded"
  },
  {
    "name": "AI Agent / MCP / LLM Infra",
    "file": "AI_Agent-MCP-LLM_Infra.txt",
    "description": "Agents, MCP, coding tools, orchestration, and LLM infrastructure.",
    "visibility": "public"
  }
]
```

## Per-list text files

Each text file is referenced by the spec's `file` field and contains one repo slug per line:

```text
owner-one/repo-one
owner-two/repo-two
owner-three/repo-three
```

Rules:

- Keep one repo per line.
- Do not include bullets.
- Blank lines are allowed.
- The same repo must not appear in multiple target files.

## Reuse strategy

Use `reuse_from` when the account is already close to GitHub's 32-list cap. The sync script will:

1. Find the existing List named in `reuse_from`
2. Rename it to the new `name`
3. Update its description and visibility
4. Reassign repos into it according to the local plan

If `reuse_from` is omitted and the target List does not exist, the script will try to create a new List.

## Exact target mode

When running:

```bash
python3 scripts/sync_github_lists.py ... --enforce-exact-targets
```

the script will remove target-list memberships for repos that are not part of the final local plan. This is useful after reusing old Lists that still contain stale members.
