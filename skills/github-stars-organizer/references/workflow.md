# GitHub Stars Workflow

## Recommended session shape

1. Confirm the target GitHub account and whether the user wants analysis only or direct mutations.
2. Ask for a classic PAT and keep it in `GITHUB_TOKEN`.
3. Export a backup before any destructive step.
4. Classify repos into themed buckets and write the local plan.
5. Review cleanup candidates with the user.
6. Unstar only the approved repos.
7. Sync the final local plan into GitHub Lists.
8. Delete old Lists only after the final Lists are verified.
9. Tell the user to revoke the token.

## Token guidance

- For export-only work, a token with `public_repo` is usually enough for public stars.
- For List creation, List updates, List deletion, or broad star management, use `user` + `public_repo`.
- Avoid fine-grained PATs for bulk star cleanup. They may not be able to unstar public repos the user does not own.
- Never store tokens in the skill directory, reference files, or reports.

## Export step

Typical command:

```bash
GITHUB_TOKEN=... python3 scripts/export_stars.py \
  --json-out /tmp/<user>-starred-backup.json \
  --csv-out /tmp/<user>-starred-backup.csv
```

Use `--limit` when smoke-testing the export logic:

```bash
GITHUB_TOKEN=... python3 scripts/export_stars.py \
  --json-out /tmp/stars-sample.json \
  --limit 10
```

## Classification heuristics

- Prefer theme-based buckets such as `Embedded / ESP32 / IoT`, `AI Agent / MCP / LLM Infra`, `Speech / Audio`, `Video / Animation / Media`, `Robotics / SLAM / RL / Embodied`, and similar user-centric groups.
- Keep public Lists broad enough to be stable over time.
- Avoid language-based buckets unless the user explicitly wants them.
- Use local-only buckets such as `Learning`, `待看`, or `Research` when the repos are still too mixed for a public List.
- If the user mainly wants to reduce noise, propose `High-confidence` and `Medium-confidence` cleanup candidates before doing any final public grouping.

## Cleanup step

The unstar input format is one repo slug per line:

```text
owner-one/repo-one
owner-two/repo-two
owner-three/repo-three
```

Dry-run first:

```bash
GITHUB_TOKEN=... python3 scripts/unstar_repos.py \
  --input /tmp/high-confidence.txt \
  --json-out /tmp/unstar-dry-run.json \
  --dry-run
```

Apply only after explicit user approval:

```bash
GITHUB_TOKEN=... python3 scripts/unstar_repos.py \
  --input /tmp/high-confidence.txt \
  --json-out /tmp/unstar-results.json \
  --tsv-out /tmp/unstar-results.tsv
```

## Syncing GitHub Lists

Prepare two things:

1. A JSON spec file that defines the target List names and file mappings.
2. A directory of text files where each file contains one `owner/repo` per line.

Dry-run:

```bash
GITHUB_TOKEN=... python3 scripts/sync_github_lists.py \
  --spec /tmp/github-lists-spec.json \
  --lists-dir /tmp/final-github-lists \
  --report /tmp/github-lists-sync-dry-run.json \
  --dry-run
```

Apply:

```bash
GITHUB_TOKEN=... python3 scripts/sync_github_lists.py \
  --spec /tmp/github-lists-spec.json \
  --lists-dir /tmp/final-github-lists \
  --report /tmp/github-lists-sync.json \
  --enforce-exact-targets
```

## GitHub-specific constraints

- GitHub currently caps user Lists at 32.
- If the user already has many Lists, use `reuse_from` in the spec to rename and repurpose old Lists instead of creating new ones.
- `--enforce-exact-targets` removes target-list memberships for repos that do not belong in the final plan, including leftovers from reused Lists.
- The sync script preserves non-target List memberships by default.

## Deleting old Lists

Only do this after the final Lists are already correct.

Dry-run:

```bash
GITHUB_TOKEN=... python3 scripts/delete_old_lists.py \
  --spec /tmp/github-lists-spec.json \
  --report /tmp/github-lists-delete-dry-run.json \
  --dry-run
```

Apply:

```bash
GITHUB_TOKEN=... python3 scripts/delete_old_lists.py \
  --spec /tmp/github-lists-spec.json \
  --report /tmp/github-lists-delete.json
```

Deleting a List does not remove stars.

## Final verification

- Check the sync report's `verified_counts`.
- Compare the GitHub List counts against the local per-list text files.
- Confirm the user still wants the old Lists removed before deleting them.
- Remind the user to revoke the PAT when the session is complete.
