#!/usr/bin/env python3
"""Check whether docs/agent exists and still looks trustworthy."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

REQUIRED_FILES = [
    'README.md',
    'START_HERE.md',
    'PROJECT_STATUS.md',
    'ARCHITECTURE.md',
    'DECISIONS.md',
    'TASKS.md',
    'CONTEXT.md',
]
PLACEHOLDER_PATTERNS = ['[TODO:', '{{', '[fill in', '[replace']


def extract_latest_handoff(project_status: str) -> str | None:
    match = re.search(r'^- Latest handoff:\s*(.+)$', project_status, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if not value or value.lower() in {'[none yet]', 'none', 'n/a'}:
        return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description='Check docs/agent health for a project.')
    parser.add_argument('--project-dir', type=Path, default=Path.cwd(), help='Project root directory')
    parser.add_argument('--max-age-days', type=int, default=7, help='Warn if PROJECT_STATUS.md is older than this')
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    docs_dir = project_dir / 'docs' / 'agent'
    handoffs_dir = docs_dir / 'handoffs'
    issues: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    if not docs_dir.exists():
        issues.append('docs/agent/ does not exist')
    else:
        for filename in REQUIRED_FILES:
            path = docs_dir / filename
            if not path.exists():
                issues.append(f'missing required file: docs/agent/{filename}')
                continue
            content = path.read_text(encoding='utf-8')
            for marker in PLACEHOLDER_PATTERNS:
                if marker in content:
                    warnings.append(f'docs/agent/{filename} still contains placeholder marker {marker}')
                    break

        if not handoffs_dir.exists():
            warnings.append('docs/agent/handoffs/ is missing')
        else:
            handoff_count = len([p for p in handoffs_dir.glob('*.md') if p.is_file()])
            notes.append(f'handoff count: {handoff_count}')

        status_file = docs_dir / 'PROJECT_STATUS.md'
        if status_file.exists():
            age = datetime.now() - datetime.fromtimestamp(status_file.stat().st_mtime)
            if age > timedelta(days=args.max_age_days):
                warnings.append(
                    f'PROJECT_STATUS.md has not been updated in {int(age.total_seconds() // 86400)} days'
                )

            status_content = status_file.read_text(encoding='utf-8')
            latest_handoff = extract_latest_handoff(status_content)
            if latest_handoff:
                latest_handoff_path = project_dir / latest_handoff
                if not latest_handoff_path.exists():
                    warnings.append(f'latest handoff path does not exist: {latest_handoff}')
                elif latest_handoff_path.stat().st_mtime > status_file.stat().st_mtime + 60:
                    warnings.append('latest handoff is newer than PROJECT_STATUS.md; status may not be synced')
            elif handoffs_dir.exists() and any(handoffs_dir.glob('*.md')):
                warnings.append('handoff files exist, but PROJECT_STATUS.md does not name the latest handoff')

    print(f'Project: {project_dir}')
    print(f'Docs dir: {docs_dir}')
    print()

    if issues:
        print('[ERROR] Issues')
        for issue in issues:
            print(f' - {issue}')
        print()

    if warnings:
        print('[WARN] Warnings')
        for warning in warnings:
            print(f' - {warning}')
        print()

    if notes:
        print('[INFO] Notes')
        for note in notes:
            print(f' - {note}')
        print()

    if issues:
        print('Verdict: docs need repair before future agents should rely on them.')
        return 1

    if warnings:
        print('Verdict: docs are usable but should be refreshed.')
        return 0

    print('Verdict: docs look healthy.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
