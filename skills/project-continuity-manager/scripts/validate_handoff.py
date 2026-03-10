#!/usr/bin/env python3
"""Validate a docs/agent handoff file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (r'ghp_[A-Za-z0-9]{36}', 'GitHub personal access token'),
    (r'sk-[A-Za-z0-9]{20,}', 'API key style token'),
    (r'Bearer\s+[A-Za-z0-9._-]+', 'Bearer token'),
    (r'-----BEGIN [A-Z ]+PRIVATE KEY-----', 'Private key block'),
    (r'password\s*[:=]\s*\S+', 'Password assignment'),
    (r'secret\s*[:=]\s*\S+', 'Secret assignment'),
    (r'token\s*[:=]\s*\S+', 'Token assignment'),
]
REQUIRED_SECTIONS = ['Current Summary', 'Immediate Next Steps', 'Important Context']
RECOMMENDED_SECTIONS = ['Files Touched This Session', 'Decisions or Discoveries']


def remaining_todos(content: str) -> list[str]:
    return re.findall(r'\[TODO:[^\]]*\]', content)


def section_content(content: str, heading: str) -> str | None:
    pattern = re.compile(rf'(^##\s+{re.escape(heading)}\s*$)', re.MULTILINE)
    match = pattern.search(content)
    if not match:
        return None
    start = match.end()
    next_match = re.search(r'^##\s+', content[start:], re.MULTILINE)
    end = start + next_match.start() if next_match else len(content)
    return content[start:end].strip()


def scan_for_secrets(content: str) -> list[str]:
    findings = []
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            findings.append(label)
    return findings


def check_file_references(content: str, project_root: Path) -> list[str]:
    candidates = set()
    for match in re.findall(r'`([A-Za-z0-9_./-]+\.[A-Za-z0-9]+(?::\d+)?)`', content):
        candidates.add(match.split(':')[0])
    for match in re.findall(r'^\|\s*([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)\s*\|', content, re.MULTILINE):
        candidates.add(match)

    missing = []
    for candidate in sorted(candidates):
        if candidate.startswith('http'):
            continue
        if '/' not in candidate:
            continue
        if not (project_root / candidate).exists():
            missing.append(candidate)
    return missing


def project_root_for_handoff(handoff_file: Path) -> Path:
    try:
        return handoff_file.parents[3]
    except IndexError:
        return handoff_file.parent


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python3 validate_handoff.py <handoff-file>')
        return 1

    handoff_file = Path(sys.argv[1]).resolve()
    if not handoff_file.exists():
        print(f'Error: file not found: {handoff_file}')
        return 1

    content = handoff_file.read_text(encoding='utf-8')
    todos = remaining_todos(content)
    missing_required = []
    for heading in REQUIRED_SECTIONS:
        section = section_content(content, heading)
        if not section or len(section) < 40 or '[TODO:' in section:
            missing_required.append(heading)

    missing_recommended = []
    for heading in RECOMMENDED_SECTIONS:
        if section_content(content, heading) is None:
            missing_recommended.append(heading)

    secrets = scan_for_secrets(content)
    missing_files = check_file_references(content, project_root_for_handoff(handoff_file))

    score = 100
    if todos:
        score -= 25
    score -= 15 * len(missing_required)
    if secrets:
        score -= 25
    score -= min(10, 2 * len(missing_files))
    score -= 2 * len(missing_recommended)
    score = max(score, 0)

    print(f'Handoff: {handoff_file}')
    print(f'Quality score: {score}/100')
    print()

    if todos:
        print('[FAIL] Remaining TODO placeholders:')
        for todo in todos[:8]:
            print(f' - {todo}')
        print()
    else:
        print('[OK] No TODO placeholders remain')
        print()

    if missing_required:
        print('[FAIL] Required sections need work:')
        for heading in missing_required:
            print(f' - {heading}')
        print()
    else:
        print('[OK] Required sections are populated')
        print()

    if secrets:
        print('[WARN] Possible secrets detected:')
        for finding in secrets:
            print(f' - {finding}')
        print()
    else:
        print('[OK] No obvious secrets detected')
        print()

    if missing_files:
        print('[WARN] Referenced files not found:')
        for item in missing_files[:10]:
            print(f' - {item}')
        print()
    else:
        print('[OK] Referenced files look valid or none were checked')
        print()

    if missing_recommended:
        print('[INFO] Recommended sections missing:')
        for heading in missing_recommended:
            print(f' - {heading}')
        print()

    ready = score >= 70 and not todos and not missing_required and not secrets
    print('Verdict: ' + ('READY for handoff' if ready else 'NEEDS WORK before handoff'))
    return 0 if ready else 1


if __name__ == '__main__':
    raise SystemExit(main())
