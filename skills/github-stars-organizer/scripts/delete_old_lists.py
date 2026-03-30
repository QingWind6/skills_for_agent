#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Set

from github_api import GitHubGraphQLClient, require_token


def load_keep_names(spec_path: str) -> Set[str]:
    raw = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    entries = raw["lists"] if isinstance(raw, dict) else raw
    keep: Set[str] = set()
    for entry in entries:
        keep.add(str(entry["name"]).strip())
    return keep


def fetch_lists(client: GitHubGraphQLClient) -> dict:
    query = """
    query {
      viewer {
        login
        lists(first: 100) {
          totalCount
          nodes {
            id
            name
            description
            isPrivate
            items(first: 1) {
              totalCount
            }
          }
        }
      }
    }
    """
    return client.call(query)["viewer"]


def delete_user_list(client: GitHubGraphQLClient, list_id: str) -> None:
    mutation = """
    mutation($input: DeleteUserListInput!) {
      deleteUserList(input: $input) {
        user {
          login
        }
      }
    }
    """
    client.call(mutation, {"input": {"listId": list_id}})


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete old GitHub Lists while keeping the final categorized lists.")
    parser.add_argument("--spec", help="JSON spec whose list names should be kept.")
    parser.add_argument("--keep-list", action="append", default=[], help="List name to keep. Repeatable.")
    parser.add_argument("--report", default="github-lists-delete-report.json", help="Write a JSON report to this path.")
    parser.add_argument("--dry-run", action="store_true", help="Only report what would be deleted.")
    parser.add_argument("--allow-delete-all", action="store_true", help="Permit deletion even when no keep names are provided.")
    parser.add_argument("--pause-seconds", type=float, default=0.05, help="Delay between GitHub API requests.")
    args = parser.parse_args()

    keep_names: Set[str] = set()
    if args.spec:
        keep_names |= load_keep_names(args.spec)
    keep_names |= {name.strip() for name in args.keep_list if name.strip()}
    if not keep_names and not args.allow_delete_all:
        parser.error("refusing to continue without keep names; pass --spec or --keep-list, or use --allow-delete-all")

    token = require_token()
    client = GitHubGraphQLClient(token, pause_seconds=args.pause_seconds)
    before = fetch_lists(client)

    delete_candidates: List[dict] = []
    for item in before["lists"]["nodes"]:
        if item["name"] in keep_names:
            continue
        delete_candidates.append(
            {
                "id": item["id"],
                "name": item["name"],
                "description": item.get("description", ""),
                "isPrivate": item["isPrivate"],
                "itemCount": item["items"]["totalCount"],
            }
        )

    deleted: List[dict] = []
    if not args.dry_run:
        for item in delete_candidates:
            delete_user_list(client, item["id"])
            deleted.append(item)

    after = None if args.dry_run else fetch_lists(client)
    report = {
        "viewer": before["login"],
        "dry_run": args.dry_run,
        "keep_names": sorted(keep_names),
        "before_total_count": before["lists"]["totalCount"],
        "delete_candidate_count": len(delete_candidates),
        "delete_candidates": delete_candidates,
        "deleted_count": len(deleted),
        "deleted_lists": deleted,
        "after_total_count": None if after is None else after["lists"]["totalCount"],
        "remaining_lists": None
        if after is None
        else [
            {
                "id": item["id"],
                "name": item["name"],
                "itemCount": item["items"]["totalCount"],
            }
            for item in after["lists"]["nodes"]
        ],
    }

    report_path = Path(args.report)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "viewer": before["login"],
                "dry_run": args.dry_run,
                "delete_candidate_count": len(delete_candidates),
                "deleted_count": len(deleted),
                "remaining_count": None if after is None else after["lists"]["totalCount"],
                "report": str(report_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
