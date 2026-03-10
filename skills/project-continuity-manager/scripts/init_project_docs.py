#!/usr/bin/env python3
"""Initialize docs/agent for a long-running project."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

TEMPLATE_NAMES = [
    'README.template.md',
    'START_HERE.template.md',
    'PROJECT_STATUS.template.md',
    'ARCHITECTURE.template.md',
    'DECISIONS.template.md',
    'TASKS.template.md',
    'CONTEXT.template.md',
]


def template_dir() -> Path:
    return Path(__file__).resolve().parent.parent / 'assets' / 'templates'


def render_template(content: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        content = content.replace('{{' + key + '}}', value)
    return content


def write_if_allowed(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return 'skipped'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return 'written'


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Initialize docs/agent templates for a long-running project.'
    )
    parser.add_argument('--project-dir', type=Path, default=Path.cwd(), help='Project root directory')
    parser.add_argument('--project-name', default=None, help='Project name (defaults to directory name)')
    parser.add_argument('--description', default='', help='Short project description')
    parser.add_argument('--tech-stack', default='', help='Comma-separated or prose tech stack summary')
    parser.add_argument('--primary-goal', default='Define the first meaningful milestone', help='Current primary goal')
    parser.add_argument('--force', action='store_true', help='Overwrite existing docs if they already exist')
    args = parser.parse_args()

    project_dir = args.project_dir.resolve()
    if not project_dir.exists():
        print(f'Error: project directory does not exist: {project_dir}', file=sys.stderr)
        return 1

    project_name = args.project_name or project_dir.name
    docs_dir = project_dir / 'docs' / 'agent'
    handoffs_dir = docs_dir / 'handoffs'
    today = datetime.now().strftime('%Y-%m-%d')

    replacements = {
        'PROJECT_NAME': project_name,
        'PROJECT_DESCRIPTION': args.description or '[fill in project description]',
        'TECH_STACK': args.tech_stack or '[fill in tech stack]',
        'PRIMARY_GOAL': args.primary_goal or '[fill in current primary goal]',
        'DATE': today,
    }

    source_dir = template_dir()
    if not source_dir.exists():
        print(f'Error: template directory not found: {source_dir}', file=sys.stderr)
        return 1

    docs_dir.mkdir(parents=True, exist_ok=True)
    handoffs_dir.mkdir(parents=True, exist_ok=True)

    print(f'Initializing docs in: {docs_dir}')
    results: list[tuple[str, Path]] = []
    for template_name in TEMPLATE_NAMES:
        source = source_dir / template_name
        if not source.exists():
            print(f'Warning: missing template: {source}', file=sys.stderr)
            continue
        destination = docs_dir / template_name.replace('.template', '')
        content = render_template(source.read_text(encoding='utf-8'), replacements)
        outcome = write_if_allowed(destination, content, args.force)
        results.append((outcome, destination))

    gitkeep = handoffs_dir / '.gitkeep'
    if not gitkeep.exists() or args.force:
        gitkeep.write_text('', encoding='utf-8')
        results.append(('written', gitkeep))
    else:
        results.append(('skipped', gitkeep))

    written = 0
    skipped = 0
    for outcome, path in results:
        label = '[OK]' if outcome == 'written' else '[SKIP]'
        print(f'{label} {path.relative_to(project_dir)}')
        if outcome == 'written':
            written += 1
        else:
            skipped += 1

    print()
    print(f'Created or updated {written} item(s); skipped {skipped} existing item(s).')
    print('Next steps:')
    print('1. Review docs/agent/START_HERE.md and PROJECT_STATUS.md')
    print('2. Fill the placeholders that matter for your project')
    print('3. Commit docs/agent/ so future agents can rely on it')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
