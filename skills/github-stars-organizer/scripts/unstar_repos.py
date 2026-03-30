#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List
from urllib.parse import quote

from github_api import GitHubRESTClient, require_token


def load_repos(path: Path, max_repos: int) -> List[str]:
    repos: List[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        repo = line.split()[0]
        if "/" not in repo:
            raise RuntimeError(f"invalid repo slug: {repo}")
        repos.append(repo)
        if max_repos and len(repos) >= max_repos:
            break
    return repos


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: List[dict]) -> None:
    lines = ["repo\tstatus"]
    for row in rows:
        lines.append(f"{row['repo']}\t{row['status']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-unstar GitHub repositories from a text file.")
    parser.add_argument("--input", required=True, help="Text file containing one owner/repo per line.")
    parser.add_argument("--json-out", help="Write a JSON report to this path.")
    parser.add_argument("--tsv-out", help="Write a TSV report to this path.")
    parser.add_argument("--dry-run", action="store_true", help="Plan changes without unstarring anything.")
    parser.add_argument("--max-repos", type=int, default=0, help="Only process the first N repos from the input file.")
    parser.add_argument("--pause-seconds", type=float, default=0.0, help="Delay between API requests.")
    args = parser.parse_args()

    token = require_token()
    client = GitHubRESTClient(token, pause_seconds=args.pause_seconds)
    repos = load_repos(Path(args.input), args.max_repos)

    rows: List[dict] = []
    success_count = 0
    missing_count = 0
    dry_run_count = 0

    for repo in repos:
        if args.dry_run:
            rows.append({"repo": repo, "status": "dry-run"})
            dry_run_count += 1
            continue

        owner, name = repo.split("/", 1)
        status, _ = client.request_status(
            "DELETE",
            f"/user/starred/{quote(owner, safe='')}/{quote(name, safe='')}",
        )
        if status == 204:
            rows.append({"repo": repo, "status": "unstarred"})
            success_count += 1
        elif status == 404:
            rows.append({"repo": repo, "status": "not-starred-or-not-found"})
            missing_count += 1
        else:
            raise RuntimeError(f"unexpected status for {repo}: {status}")

    report = {
        "input": args.input,
        "dry_run": args.dry_run,
        "repo_count": len(repos),
        "unstarred_count": success_count,
        "not_starred_or_not_found_count": missing_count,
        "dry_run_count": dry_run_count,
        "results": rows,
    }

    if args.json_out:
        write_json(Path(args.json_out), report)
    if args.tsv_out:
        write_tsv(Path(args.tsv_out), rows)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
