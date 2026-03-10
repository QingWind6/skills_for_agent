#!/usr/bin/env python3
"""Check whether a handoff is still fresh enough to trust."""

from __future__ import annotations

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


def parse_metadata(content: str) -> dict[str, object]:
    data: dict[str, object] = {
        'created': None,
        'project': None,
        'branch': None,
        'files': [],
    }
    created = re.search(r'^- Created:\s*(.+)$', content, re.MULTILINE)
    project = re.search(r'^- Project:\s*(.+)$', content, re.MULTILINE)
    branch = re.search(r'^- Branch:\s*(.+)$', content, re.MULTILINE)
    if created:
        try:
            data['created'] = datetime.strptime(created.group(1).strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    if project:
        data['project'] = project.group(1).strip()
    if branch:
        data['branch'] = branch.group(1).strip()

    files = []
    for item in re.findall(r'^\|\s*([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)\s*\|', content, re.MULTILINE):
        if item.lower() == 'file' or item.startswith('[no modified files'):
            continue
        files.append(item)
    data['files'] = sorted(set(files))
    return data


def compute_level(days_old: float, commits_since: int, changed_files: int, branch_matches: bool, missing_files: int) -> tuple[str, list[str]]:
    score = 0
    issues = []
    if days_old > 30:
        score += 3
        issues.append(f'handoff is {int(days_old)} days old')
    elif days_old > 7:
        score += 2
        issues.append(f'handoff is {int(days_old)} days old')
    elif days_old > 1:
        score += 1

    if commits_since > 50:
        score += 3
        issues.append(f'{commits_since} commits landed after the handoff')
    elif commits_since > 20:
        score += 2
        issues.append(f'{commits_since} commits landed after the handoff')
    elif commits_since > 5:
        score += 1

    if changed_files > 20:
        score += 2
        issues.append(f'{changed_files} files changed after the handoff')
    elif changed_files > 5:
        score += 1

    if not branch_matches:
        score += 2
        issues.append('current branch differs from the handoff branch')

    if missing_files > 5:
        score += 2
        issues.append(f'{missing_files} referenced files no longer exist')
    elif missing_files > 0:
        score += 1
        issues.append(f'{missing_files} referenced file(s) are missing')

    if score == 0:
        return 'FRESH', issues
    if score <= 2:
        return 'SLIGHTLY_STALE', issues
    if score <= 4:
        return 'STALE', issues
    return 'VERY_STALE', issues


def commits_after(project_dir: Path, created: datetime | None) -> list[tuple[int, str, str]]:
    if created is None:
        return []

    ok_log, log_output = run_cmd(
        ['git', 'log', '--format=%ct%x09%H%x09%s', '--no-decorate'],
        project_dir,
    )
    if not ok_log or not log_output:
        return []

    cutoff = int(created.timestamp())
    commits: list[tuple[int, str, str]] = []
    for line in log_output.splitlines():
        parts = line.split('\t', 2)
        if len(parts) != 3:
            continue
        try:
            commit_ts = int(parts[0])
        except ValueError:
            continue
        if commit_ts > cutoff:
            commits.append((commit_ts, parts[1], parts[2]))
    return commits


def changed_files_for_commits(project_dir: Path, commits: list[tuple[int, str, str]]) -> list[str]:
    changed_files: set[str] = set()
    for _, sha, _ in commits:
        ok_show, show_output = run_cmd(['git', 'show', '--name-only', '--pretty=format:', sha], project_dir)
        if not ok_show or not show_output:
            continue
        for line in show_output.splitlines():
            line = line.strip()
            if line:
                changed_files.add(line)
    return sorted(changed_files)


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python3 check_handoff_freshness.py <handoff-file>')
        return 1

    handoff_file = Path(sys.argv[1]).resolve()
    if not handoff_file.exists():
        print(f'Error: file not found: {handoff_file}')
        return 1

    content = handoff_file.read_text(encoding='utf-8')
    meta = parse_metadata(content)
    try:
        fallback_project = handoff_file.parents[3]
    except IndexError:
        fallback_project = handoff_file.parent
    project_dir = Path(str(meta['project'])) if meta['project'] else fallback_project
    created = meta['created']

    if not project_dir.exists():
        print(f'Error: project path is missing: {project_dir}')
        return 1

    ok_repo, _ = run_cmd(['git', 'rev-parse', '--git-dir'], project_dir)
    current_branch = None
    commits_since = 0
    changed_files: list[str] = []
    branch_matches = True

    if ok_repo:
        ok_branch, branch_output = run_cmd(['git', 'branch', '--show-current'], project_dir)
        current_branch = branch_output if ok_branch and branch_output else '[unknown]'
        handoff_branch = str(meta['branch']) if meta['branch'] else None
        if handoff_branch and not handoff_branch.startswith('['):
            branch_matches = current_branch == handoff_branch

        filtered_commits = commits_after(project_dir, created)
        commits_since = len(filtered_commits)
        changed_files = changed_files_for_commits(project_dir, filtered_commits)

    referenced_files = [Path(project_dir) / item for item in meta['files']]
    missing_refs = [str(path.relative_to(project_dir)) for path in referenced_files if not path.exists()]
    days_old = (datetime.now() - created).total_seconds() / 86400 if created else 0.0
    level, issues = compute_level(days_old, commits_since, len(changed_files), branch_matches, len(missing_refs))

    print(f'Handoff: {handoff_file}')
    print(f'Project: {project_dir}')
    if created:
        print(f'Created: {created.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Freshness: {level}')
    print()

    if current_branch is not None:
        print(f'- Current branch: {current_branch}')
    if meta['branch']:
        print(f'- Handoff branch: {meta["branch"]}')
    print(f'- Commits since handoff: {commits_since}')
    print(f'- Files changed since handoff: {len(changed_files)}')
    print(f'- Missing referenced files: {len(missing_refs)}')
    print()

    if issues:
        print('Issues:')
        for issue in issues:
            print(f' - {issue}')
        print()

    if level == 'FRESH':
        print('Verdict: safe to resume directly.')
        return 0
    if level == 'SLIGHTLY_STALE':
        print('Verdict: review recent changes, then resume.')
        return 0
    if level == 'STALE':
        print('Verdict: verify the code and status docs carefully before resuming.')
        return 1

    print('Verdict: create a new handoff or refresh docs before trusting this fully.')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
