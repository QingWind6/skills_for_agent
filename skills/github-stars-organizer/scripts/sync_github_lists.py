#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

from github_api import GitHubGraphQLClient, require_token


def parse_visibility(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    normalized = str(value).strip().lower()
    if normalized in {"private", "true", "1", "yes"}:
        return True
    if normalized in {"public", "false", "0", "no"}:
        return False
    raise RuntimeError(f"invalid visibility value: {value!r}")


def load_spec(path: Path) -> List[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = raw["lists"] if isinstance(raw, dict) else raw
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("spec must be a non-empty list or an object containing a non-empty 'lists' array")

    normalized: List[dict] = []
    seen_names: Set[str] = set()

    for entry in entries:
        if not isinstance(entry, dict):
            raise RuntimeError("every spec entry must be an object")
        name = str(entry.get("name", "")).strip()
        file_name = str(entry.get("file", "")).strip()
        description = str(entry.get("description", "")).strip()
        reuse_from = entry.get("reuse_from")
        if reuse_from is not None:
            reuse_from = str(reuse_from).strip()

        if not name or not file_name:
            raise RuntimeError("each spec entry requires non-empty 'name' and 'file'")
        if name in seen_names:
            raise RuntimeError(f"duplicate list name in spec: {name}")
        seen_names.add(name)

        normalized.append(
            {
                "name": name,
                "file": file_name,
                "description": description,
                "visibility": parse_visibility(entry.get("visibility", "public")),
                "reuse_from": reuse_from or None,
            }
        )

    return normalized


def load_assignments(specs: List[dict], lists_dir: Path) -> Tuple[Dict[str, List[str]], Dict[str, str]]:
    repos_by_list: Dict[str, List[str]] = {}
    list_by_repo: Dict[str, str] = {}

    for spec in specs:
        path = lists_dir / spec["file"]
        if not path.exists():
            raise RuntimeError(f"missing list file: {path}")

        repos: List[str] = []
        for raw in path.read_text(encoding="utf-8").splitlines():
            repo = raw.strip()
            if not repo:
                continue
            if "/" not in repo:
                raise RuntimeError(f"invalid repo slug in {path}: {repo}")
            if repo in list_by_repo and list_by_repo[repo] != spec["name"]:
                raise RuntimeError(
                    f"repo assigned to multiple target lists: {repo} -> "
                    f"{list_by_repo[repo]!r}, {spec['name']!r}"
                )
            repos.append(repo)
            list_by_repo[repo] = spec["name"]

        repos_by_list[spec["name"]] = repos

    return repos_by_list, list_by_repo


def fetch_viewer_lists(client: GitHubGraphQLClient) -> Tuple[str, List[dict]]:
    query = """
    query($after: String) {
      viewer {
        login
        lists(first: 100, after: $after) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            name
            slug
            description
            isPrivate
          }
        }
      }
    }
    """
    after = None
    login: Optional[str] = None
    lists: List[dict] = []

    while True:
        data = client.call(query, {"after": after})
        viewer = data["viewer"]
        if login is None:
            login = viewer["login"]
        page = viewer["lists"]
        lists.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    assert login is not None
    return login, lists


def fetch_list_items(client: GitHubGraphQLClient, list_id: str) -> List[dict]:
    query = """
    query($id: ID!, $after: String) {
      node(id: $id) {
        ... on UserList {
          items(first: 100, after: $after) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              __typename
              ... on Repository {
                id
                nameWithOwner
              }
            }
          }
        }
      }
    }
    """
    items: List[dict] = []
    after = None
    while True:
        data = client.call(query, {"id": list_id, "after": after})
        page = data["node"]["items"]
        for item in page["nodes"] or []:
            if item and item.get("__typename") == "Repository":
                items.append(item)
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return items


def create_user_list(client: GitHubGraphQLClient, spec: dict) -> dict:
    mutation = """
    mutation($input: CreateUserListInput!) {
      createUserList(input: $input) {
        list {
          id
          name
          slug
          description
          isPrivate
        }
      }
    }
    """
    data = client.call(
        mutation,
        {
            "input": {
                "name": spec["name"],
                "description": spec["description"],
                "isPrivate": spec["visibility"],
            }
        },
    )
    return data["createUserList"]["list"]


def update_user_list(client: GitHubGraphQLClient, list_id: str, spec: dict) -> dict:
    mutation = """
    mutation($input: UpdateUserListInput!) {
      updateUserList(input: $input) {
        list {
          id
          name
          slug
          description
          isPrivate
        }
      }
    }
    """
    data = client.call(
        mutation,
        {
            "input": {
                "listId": list_id,
                "name": spec["name"],
                "description": spec["description"],
                "isPrivate": spec["visibility"],
            }
        },
    )
    return data["updateUserList"]["list"]


def resolve_repo_ids(client: GitHubGraphQLClient, repos: Iterable[str], chunk_size: int = 20) -> Dict[str, str]:
    repos = list(repos)
    resolved: Dict[str, str] = {}

    for start in range(0, len(repos), chunk_size):
        chunk = repos[start : start + chunk_size]
        lines = ["query {"]
        alias_to_repo: Dict[str, str] = {}
        for idx, repo in enumerate(chunk):
            owner, name = repo.split("/", 1)
            alias = f"r{idx}"
            alias_to_repo[alias] = repo
            lines.append(
                f"  {alias}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) "
                "{ id nameWithOwner }"
            )
        lines.append("}")
        data = client.call("\n".join(lines))
        for alias, repo in alias_to_repo.items():
            node = data.get(alias)
            if node is None:
                raise RuntimeError(f"repository lookup failed: {repo}")
            resolved[repo] = node["id"]
    return resolved


def update_item_lists(client: GitHubGraphQLClient, repo_id: str, repo_slug: str, list_ids: List[str]) -> List[dict]:
    mutation = """
    mutation($input: UpdateUserListsForItemInput!) {
      updateUserListsForItem(input: $input) {
        item {
          __typename
          ... on Repository {
            nameWithOwner
          }
        }
        lists {
          id
          name
        }
      }
    }
    """
    data = client.call(
        mutation,
        {
            "input": {
                "itemId": repo_id,
                "listIds": list_ids,
            }
        },
    )
    item = data["updateUserListsForItem"]["item"]
    if item is None or item.get("__typename") != "Repository":
        raise RuntimeError(f"unexpected update response for {repo_slug}")
    if item["nameWithOwner"].lower() != repo_slug.lower():
        raise RuntimeError(f"updated wrong repository: expected {repo_slug}, got {item['nameWithOwner']}")
    return data["updateUserListsForItem"]["lists"] or []


def build_existing_memberships(
    client: GitHubGraphQLClient,
    existing_lists: List[dict],
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]], Dict[str, str]]:
    list_ids_by_repo_id: Dict[str, Set[str]] = defaultdict(set)
    list_names_by_repo_slug: Dict[str, Set[str]] = defaultdict(set)
    repo_slug_by_id: Dict[str, str] = {}

    for user_list in existing_lists:
        items = fetch_list_items(client, user_list["id"])
        for item in items:
            repo_id = item["id"]
            repo_slug = item["nameWithOwner"]
            list_ids_by_repo_id[repo_id].add(user_list["id"])
            list_names_by_repo_slug[repo_slug].add(user_list["name"])
            repo_slug_by_id[repo_id] = repo_slug

    return list_ids_by_repo_id, list_names_by_repo_slug, repo_slug_by_id


def verify_target_counts(client: GitHubGraphQLClient, target_lists: Dict[str, dict]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for list_name, metadata in target_lists.items():
        counts[list_name] = len(fetch_list_items(client, metadata["id"]))
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync local repo groups into GitHub Lists.")
    parser.add_argument("--spec", required=True, help="JSON spec describing the target GitHub Lists.")
    parser.add_argument("--lists-dir", required=True, help="Directory containing one owner/repo text file per list.")
    parser.add_argument("--report", default="github-lists-sync-report.json", help="Write a JSON report to this path.")
    parser.add_argument("--dry-run", action="store_true", help="Compute the plan without mutating GitHub.")
    parser.add_argument(
        "--enforce-exact-targets",
        action="store_true",
        help="Remove target-list memberships for repos that are not present in the local plan.",
    )
    parser.add_argument("--pause-seconds", type=float, default=0.05, help="Delay between GitHub API requests.")
    args = parser.parse_args()

    token = require_token()
    specs = load_spec(Path(args.spec))
    repos_by_list, final_list_by_repo = load_assignments(specs, Path(args.lists_dir))
    client = GitHubGraphQLClient(token, pause_seconds=args.pause_seconds)

    viewer_login, existing_lists = fetch_viewer_lists(client)
    existing_by_name = {item["name"]: item for item in existing_lists}
    list_ids_by_repo_id, list_names_by_repo_slug, repo_slug_by_id = build_existing_memberships(client, existing_lists)

    target_lists: Dict[str, dict] = {}
    created_lists: List[dict] = []
    reused_lists: List[dict] = []
    updated_target_lists: List[dict] = []

    for spec in specs:
        existing = existing_by_name.get(spec["name"])
        if existing:
            needs_update = (
                existing.get("description", "") != spec["description"]
                or bool(existing.get("isPrivate")) != bool(spec["visibility"])
            )
            if needs_update:
                updated = (
                    {
                        **existing,
                        "description": spec["description"],
                        "isPrivate": spec["visibility"],
                    }
                    if args.dry_run
                    else update_user_list(client, existing["id"], spec)
                )
                target_lists[spec["name"]] = updated
                updated_target_lists.append(updated)
            else:
                target_lists[spec["name"]] = existing
            continue

        reuse_from = spec.get("reuse_from")
        reusable = existing_by_name.get(reuse_from) if reuse_from else None
        if reusable and reusable["name"] not in target_lists:
            updated = (
                {
                    "id": reusable["id"],
                    "name": spec["name"],
                    "slug": reusable.get("slug"),
                    "description": spec["description"],
                    "isPrivate": spec["visibility"],
                    "reused_from": reusable["name"],
                }
                if args.dry_run
                else update_user_list(client, reusable["id"], spec)
            )
            updated["reused_from"] = reusable["name"]
            target_lists[spec["name"]] = updated
            reused_lists.append(updated)
            continue

        if args.dry_run:
            target_lists[spec["name"]] = {
                "id": None,
                "name": spec["name"],
                "slug": None,
                "description": spec["description"],
                "isPrivate": spec["visibility"],
            }
            continue

        created = create_user_list(client, spec)
        target_lists[spec["name"]] = created
        created_lists.append(created)

    repo_ids = resolve_repo_ids(client, final_list_by_repo.keys())
    repo_slug_by_id.update({repo_id: repo for repo, repo_id in repo_ids.items()})

    desired_by_repo_id: Dict[str, Set[str]] = {}
    reason_by_repo_id: Dict[str, Set[str]] = defaultdict(set)

    for repo_slug, target_list_name in sorted(final_list_by_repo.items()):
        repo_id = repo_ids[repo_slug]
        current = set(list_ids_by_repo_id.get(repo_id, set()))
        desired = set(desired_by_repo_id.get(repo_id, current))
        target_list_id = target_lists[target_list_name]["id"]
        if target_list_id is not None and target_list_id not in desired:
            desired.add(target_list_id)
            reason_by_repo_id[repo_id].add(f"add-target:{target_list_name}")
        desired_by_repo_id[repo_id] = desired

    if args.enforce_exact_targets:
        for list_name, metadata in target_lists.items():
            target_id = metadata.get("id")
            if target_id is None:
                continue
            for item in fetch_list_items(client, target_id):
                repo_id = item["id"]
                repo_slug = item["nameWithOwner"]
                repo_slug_by_id[repo_id] = repo_slug
                expected_list_name = final_list_by_repo.get(repo_slug)
                if expected_list_name == list_name:
                    continue
                current = set(desired_by_repo_id.get(repo_id, list_ids_by_repo_id.get(repo_id, set())))
                if target_id in current:
                    current.remove(target_id)
                    desired_by_repo_id[repo_id] = current
                    reason_by_repo_id[repo_id].add(f"remove-extra:{list_name}")

    current_name_by_id = {item["id"]: item["name"] for item in existing_lists}
    current_name_by_id.update({item["id"]: item["name"] for item in target_lists.values() if item.get("id")})

    planned_updates: List[dict] = []
    skipped_updates: List[dict] = []

    for repo_id, desired in sorted(desired_by_repo_id.items(), key=lambda item: repo_slug_by_id[item[0]].lower()):
        current = set(list_ids_by_repo_id.get(repo_id, set()))
        repo_slug = repo_slug_by_id[repo_id]
        entry = {
            "repo": repo_slug,
            "repo_id": repo_id,
            "reasons": sorted(reason_by_repo_id.get(repo_id, set())),
            "current_list_ids": sorted(current),
            "current_list_names": sorted(list_names_by_repo_slug.get(repo_slug, set())),
            "desired_list_ids": sorted(desired),
            "desired_list_names": [current_name_by_id[list_id] for list_id in sorted(desired)],
        }
        if current == desired:
            skipped_updates.append(entry)
        else:
            planned_updates.append(entry)

    applied_updates: List[dict] = []
    if not args.dry_run:
        for entry in planned_updates:
            updated_lists = update_item_lists(
                client,
                repo_id=entry["repo_id"],
                repo_slug=entry["repo"],
                list_ids=entry["desired_list_ids"],
            )
            enriched = dict(entry)
            enriched["updated_list_names"] = [item["name"] for item in updated_lists]
            applied_updates.append(enriched)

    report = {
        "viewer": viewer_login,
        "dry_run": args.dry_run,
        "enforce_exact_targets": args.enforce_exact_targets,
        "target_list_count": len(specs),
        "created_lists": created_lists,
        "reused_lists": reused_lists,
        "updated_target_lists": updated_target_lists,
        "expected_counts": {name: len(repos) for name, repos in repos_by_list.items()},
        "planned_update_count": len(planned_updates),
        "skipped_update_count": len(skipped_updates),
        "planned_updates": planned_updates,
        "skipped_updates": skipped_updates,
        "applied_update_count": len(applied_updates),
        "applied_updates": applied_updates,
        "verified_counts": None if args.dry_run else verify_target_counts(client, target_lists),
    }
    report_path = Path(args.report)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "viewer": viewer_login,
                "dry_run": args.dry_run,
                "created_list_count": len(created_lists),
                "reused_list_count": len(reused_lists),
                "updated_target_list_count": len(updated_target_lists),
                "planned_update_count": len(planned_updates),
                "skipped_update_count": len(skipped_updates),
                "verified_counts": report["verified_counts"],
                "report": str(report_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
