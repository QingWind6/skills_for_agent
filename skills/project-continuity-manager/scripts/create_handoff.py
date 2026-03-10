#!/usr/bin/env python3
"""Create a timestamped handoff in docs/agent/handoffs/."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: list[str], cwd: Path) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, ''
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output


def template_path() -> Path:
    return Path(__file__).resolve().parent.parent / 'assets' / 'templates' / 'HANDOFF.template.md'


def sanitize_slug(slug: str | None) -> str:
    if not slug:
        return 'session'
    slug = slug.strip().lower().replace(' ', '-').replace('_', '-')
    slug = re.sub(r'[^a-z0-9-]+', '', slug)
    slug = re.sub(r'-{2,}', '-', slug).strip('-')
    return slug or 'session'


def humanize_slug(slug: str) -> str:
    return slug.replace('-', ' ').strip().title() or 'Session Handoff'


def latest_handoff(handoffs_dir: Path) -> Path | None:
    candidates = sorted(handoffs_dir.glob('*.md'))
    return candidates[-1] if candidates else None


def extract_active_work(status_file: Path) -> str:
    if not status_file.exists():
        return '[missing PROJECT_STATUS.md]'
    content = status_file.read_text(encoding='utf-8')
    match = re.search(r'^- Active work:\s*(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else '[not set in PROJECT_STATUS.md]'


def git_info(project_dir: Path) -> tuple[str, list[str], list[str]]:
    ok_branch, branch = run_cmd(['git', 'branch', '--show-current'], project_dir)
    ok_log, log = run_cmd(['git', 'log', '--oneline', '-5', '--no-decorate'], project_dir)
    ok_mod, modified = run_cmd(['git', 'diff', '--name-only'], project_dir)
    ok_staged, staged = run_cmd(['git', 'diff', '--name-only', '--cached'], project_dir)

    branch_text = branch if ok_branch and branch else '[not a git repo or detached HEAD]'
    commits = log.splitlines() if ok_log and log else []
    files: list[str] = []
    if ok_mod and modified:
        files.extend(modified.splitlines())
    if ok_staged and staged:
        files.extend(staged.splitlines())
    unique_files = sorted(set(f for f in files if f))
    return branch_text, commits, unique_files


def render_recent_commits(commits: list[str]) -> str:
    if not commits:
        return '- [no recent commits detected]'
    return '\n'.join(f'- {entry}' for entry in commits)


def render_files_table(files: list[str]) -> str:
    if not files:
        return '| [no modified files detected] | [fill in if needed] | [fill in if needed] |'
    return '\n'.join(
        f'| {file_path} | [why this file matters] | [what changed] |'
        for file_path in files
    )


def main() -> int:
    parser = argparse.ArgumentParser(description='Create a new docs/agent handoff scaffold.')
    parser.add_argument('--project-dir', type=Path, default=Path.cwd(), help='Project root directory')
    parser.add_argument('--slug', default=None, help='Short topic slug, for example auth-refactor')
    parser.add_argument('--title', default=None, help='Optional human-readable handoff title')
    parser.add_argument('--continues-from', default=None, help='Filename or relative path of previous handoff')
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    docs_dir = project_dir / 'docs' / 'agent'
    status_file = docs_dir / 'PROJECT_STATUS.md'
    handoffs_dir = docs_dir / 'handoffs'
    source_template = template_path()

    if not docs_dir.exists() or not status_file.exists():
        print('Error: docs/agent/PROJECT_STATUS.md is required before creating a handoff.', file=sys.stderr)
        return 1
    if not source_template.exists():
        print(f'Error: handoff template missing: {source_template}', file=sys.stderr)
        return 1

    handoffs_dir.mkdir(parents=True, exist_ok=True)
    slug = sanitize_slug(args.slug)
    timestamp = datetime.now()
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{slug}"
    destination = handoffs_dir / f'{file_stem}.md'

    previous = args.continues_from
    if not previous:
        prior_file = latest_handoff(handoffs_dir)
        if prior_file:
            previous = prior_file.name
    continues_from = previous or '[none]'

    branch, commits, files = git_info(project_dir)
    title = args.title or humanize_slug(slug)
    active_work = extract_active_work(status_file)

    content = source_template.read_text(encoding='utf-8')
    replacements = {
        'HANDOFF_TITLE': title,
        'DATE_TIME': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'PROJECT_PATH': str(project_dir),
        'BRANCH': branch,
        'CONTINUES_FROM': continues_from,
        'ACTIVE_WORK': active_work,
        'RECENT_COMMITS': render_recent_commits(commits),
        'FILES_TOUCHED': render_files_table(files),
    }
    for key, value in replacements.items():
        content = content.replace('{{' + key + '}}', value)

    destination.write_text(content, encoding='utf-8')

    validator = Path(__file__).with_name('validate_handoff.py')
    print(f'Created handoff: {destination}')
    print('Next steps:')
    print('1. Fill the TODO fields in the handoff')
    print(f'2. Run: python3 {validator} {destination}')
    print('3. Copy this handoff path into PROJECT_STATUS.md -> Latest handoff')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
