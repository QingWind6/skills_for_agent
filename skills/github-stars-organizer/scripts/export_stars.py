#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import List, Optional

from github_api import GitHubRESTClient, require_token


CSV_FIELDS = [
    "starred_at",
    "name_with_owner",
    "html_url",
    "description",
    "language",
    "stargazers_count",
    "fork",
    "archived",
    "private",
]


def export_json(path: Path, rows: List[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_csv(path: Path, rows: List[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export the authenticated user's GitHub stars to JSON and CSV.")
    parser.add_argument("--json-out", help="Write a JSON backup to this path.")
    parser.add_argument("--csv-out", help="Write a CSV backup to this path.")
    parser.add_argument("--limit", type=int, default=0, help="Stop after exporting this many stars. 0 means all.")
    parser.add_argument("--per-page", type=int, default=100, help="GitHub page size. Max 100.")
    parser.add_argument("--pause-seconds", type=float, default=0.0, help="Delay between API requests.")
    args = parser.parse_args()

    if not args.json_out and not args.csv_out:
        parser.error("at least one of --json-out or --csv-out is required")

    token = require_token()
    client = GitHubRESTClient(token, pause_seconds=args.pause_seconds)

    _, _, viewer = client.request_json("GET", "/user")
    login = viewer["login"]

    rows: List[dict] = []
    per_page = max(1, min(args.per_page, 100))
    page = 1

    while True:
        _, _, payload = client.request_json(
            "GET",
            "/user/starred",
            query={
                "per_page": per_page,
                "page": page,
                "sort": "created",
                "direction": "desc",
            },
            accept="application/vnd.github.star+json",
        )
        if not payload:
            break

        for item in payload:
            repo = item.get("repo", item)
            rows.append(
                {
                    "starred_at": item.get("starred_at"),
                    "name_with_owner": repo["full_name"],
                    "html_url": repo["html_url"],
                    "description": repo.get("description") or "",
                    "language": repo.get("language") or "",
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "fork": bool(repo.get("fork")),
                    "archived": bool(repo.get("archived")),
                    "private": bool(repo.get("private")),
                }
            )
            if args.limit and len(rows) >= args.limit:
                break

        if args.limit and len(rows) >= args.limit:
            rows = rows[: args.limit]
            break

        if len(payload) < per_page:
            break
        page += 1

    if args.json_out:
        export_json(Path(args.json_out), rows)
    if args.csv_out:
        export_csv(Path(args.csv_out), rows)

    print(
        json.dumps(
            {
                "viewer": login,
                "count": len(rows),
                "json_out": args.json_out,
                "csv_out": args.csv_out,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
