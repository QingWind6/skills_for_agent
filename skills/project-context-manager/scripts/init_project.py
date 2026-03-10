#!/usr/bin/env python3
"""
Project Context Manager - Initialization Script

Initialize project documentation structure for multi-session development.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def create_docs_structure(project_dir: Path, project_name: str, description: str = "", tech_stack: str = ""):
    """Create docs/agent/ directory structure with templates."""

    docs_dir = project_dir / "docs" / "agent"
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Get template directory
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent / "templates"

    if not template_dir.exists():
        print(f"Error: Template directory not found: {template_dir}", file=sys.stderr)
        return False

    # Copy templates
    templates = [
        "README.template.md",
        "START_HERE.template.md",
        "PROJECT_STATUS.template.md",
        "SESSION_HANDOFF.template.md",
        "CONTEXT.template.md"
    ]

    today = datetime.now().strftime("%Y-%m-%d")

    for template_name in templates:
        template_path = template_dir / template_name
        if not template_path.exists():
            print(f"Warning: Template not found: {template_name}", file=sys.stderr)
            continue

        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace placeholders
        content = content.replace("{{PROJECT_NAME}}", project_name)
        content = content.replace("{{PROJECT_DESCRIPTION}}", description)
        content = content.replace("{{TECH_STACK}}", tech_stack)
        content = content.replace("{{DATE}}", today)

        # Write to destination
        dest_name = template_name.replace(".template", "")
        dest_path = docs_dir / dest_name

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Created: {dest_path.relative_to(project_dir)}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize project documentation for multi-session development"
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        required=True,
        help="Project root directory"
    )
    parser.add_argument(
        "--project-name",
        type=str,
        required=True,
        help="Project name"
    )
    parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Project description"
    )
    parser.add_argument(
        "--tech-stack",
        type=str,
        default="",
        help="Technology stack (comma-separated)"
    )

    args = parser.parse_args()

    # Validate project directory
    if not args.project_dir.exists():
        print(f"Error: Project directory does not exist: {args.project_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing project documentation for: {args.project_name}")
    print(f"Project directory: {args.project_dir}")
    print()

    success = create_docs_structure(
        args.project_dir,
        args.project_name,
        args.description,
        args.tech_stack
    )

    if success:
        print()
        print("✅ Project documentation initialized successfully!")
        print()
        print("Next steps:")
        print(f"1. Review and customize files in: {args.project_dir}/docs/agent/")
        print("2. Tell your agent: 'Please read docs/agent/ directory and start working.'")
    else:
        print()
        print("❌ Failed to initialize project documentation", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
