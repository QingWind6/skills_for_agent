---
name: github-stars-organizer
description: Audit, export, classify, clean up, and reorganize GitHub starred repositories into GitHub Lists. Use when Codex needs to help a user sort GitHub stars by theme or usage, generate backup files, propose cleanup candidates, bulk-unstar approved repos, sync local groupings into GitHub Lists via GraphQL, handle the 32-list cap with list reuse, or delete old Lists after migration.
---

# GitHub Stars Organizer

Organize starred repositories as a repeatable workflow: export first, classify by theme, propose cleanup candidates, sync the final groups into GitHub Lists, then optionally prune old lists. Prefer usage-based and topic-based buckets over language-based buckets unless the user explicitly wants language buckets.

## Auth And Safety

- Ask whether the user wants analysis only or direct GitHub changes.
- Use a classic PAT in `GITHUB_TOKEN`.
- Prefer `user` + `public_repo` when the session may create Lists, rename Lists, delete Lists, or unstar repos.
- Do not rely on fine-grained PATs for bulk star cleanup; they can fail on public repos not owned by the user.
- Export a backup before any destructive change.
- Require explicit approval before unstarring repos or deleting old Lists.
- Tell the user to revoke the token after the work is done.

## Quick Start

1. Export the current stars with `scripts/export_stars.py`.
2. Classify the exported repos into 5-12 high-signal topic buckets and create:
   - one JSON spec file for the target Lists
   - one `owner/repo` text file per target List
3. If the user wants cleanup, produce `High-confidence` and `Medium-confidence` unstar candidates first.
4. Only after approval, run `scripts/unstar_repos.py`.
5. Sync the final groups into GitHub Lists with `scripts/sync_github_lists.py`.
6. If the user wants to keep only the new final scheme, run `scripts/delete_old_lists.py`.

## Workflow

### 1. Export and snapshot

- Run `scripts/export_stars.py` before cleanup or relisting work.
- Keep both JSON and CSV backups when the user may want a spreadsheet review or rollback reference.
- Write artifacts into a user-specific working directory instead of the skill folder.

### 2. Classify by usage

- Group repos by how the user actually uses them: embedded, AI infra, video tools, frontend build, robotics, self-hosted infra, and similar topical buckets.
- Avoid overly granular public Lists. If a bucket is weak or mixed, keep it local-only instead of forcing a public List.
- Local-only holding buckets such as `待看`, `Learning`, `Awesome`, or `Papers` are fine during analysis, but usually should not become final public Lists.
- Build the spec and text files described in `references/spec-format.md`.

### 3. Propose cleanup candidates

- Split unstar suggestions into at least two levels such as `High-confidence` and `Medium-confidence`.
- Show candidates before changing GitHub state.
- After approval, run `scripts/unstar_repos.py` against a text file of `owner/repo` lines.

### 4. Sync GitHub Lists

- Use `scripts/sync_github_lists.py` with the spec and list directory.
- Run a dry-run first when the account already has Lists or when the spec reuses existing list names.
- Use `reuse_from` in the spec when the user is already close to GitHub's 32-list cap.
- Use `--enforce-exact-targets` when the final Lists should exactly match the local plan, including removing leftover members from reused Lists.
- Preserve existing non-target list memberships by default.

### 5. Prune old Lists

- Only delete old Lists after the new final Lists are verified.
- Run `scripts/delete_old_lists.py` with the same spec so only the target List names are kept.
- Deleting a GitHub List does not unstar the repos inside it.

## Resources

- `scripts/export_stars.py`: export the authenticated user's stars to JSON and CSV.
- `scripts/unstar_repos.py`: bulk-unstar repos from a text file after approval.
- `scripts/sync_github_lists.py`: create, update, reuse, and populate GitHub Lists from a local plan.
- `scripts/delete_old_lists.py`: delete non-final GitHub Lists while keeping the new target Lists.
- `references/workflow.md`: end-to-end operating procedure, guardrails, and command patterns.
- `references/spec-format.md`: required JSON spec format and per-list text file format.
- `references/example-spec.json`: reusable example of a nine-list theme-based setup.

## Validation

- Prefer a dry-run before mutating GitHub.
- Compare verified List counts against the local text files after sync.
- Save machine-readable reports next to the working artifacts.
