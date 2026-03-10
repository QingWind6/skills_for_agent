#!/usr/bin/env python3
"""
Project Context Manager - Status Checker

Check if project documentation is up-to-date and consistent.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta


def check_documentation(project_dir: Path) -> dict:
    """Check documentation status and return issues."""

    docs_dir = project_dir / "docs" / "agent"
    issues = []
    warnings = []

    # Check if docs directory exists
    if not docs_dir.exists():
        issues.append("docs/agent/ directory does not exist")
        return {"issues": issues, "warnings": warnings, "status": "error"}

    # Required files
    required_files = [
        "README.md",
        "START_HERE.md",
        "PROJECT_STATUS.md",
        "SESSION_HANDOFF.md",
        "CONTEXT.md"
    ]

    # Check required files exist
    for filename in required_files:
        filepath = docs_dir / filename
        if not filepath.exists():
            issues.append(f"Missing required file: {filename}")

    # Check PROJECT_STATUS.md freshness
    status_file = docs_dir / "PROJECT_STATUS.md"
    if status_file.exists():
        mtime = datetime.fromtimestamp(status_file.stat().st_mtime)
        age = datetime.now() - mtime

        if age > timedelta(days=7):
            warnings.append(f"PROJECT_STATUS.md hasn't been updated in {age.days} days")

        # Check for placeholder content
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "暂无" in content or "N/A" in content:
                warnings.append("PROJECT_STATUS.md contains placeholder content")

    # Determine overall status
    if issues:
        status = "error"
    elif warnings:
        status = "warning"
    else:
        status = "ok"

    return {
        "issues": issues,
        "warnings": warnings,
        "status": status
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check project documentation status"
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)"
    )

    args = parser.parse_args()

    print(f"Checking documentation in: {args.project_dir}")
    print()

    result = check_documentation(args.project_dir)

    # Print issues
    if result["issues"]:
        print("❌ Issues:")
        for issue in result["issues"]:
            print(f"  - {issue}")
        print()

    # Print warnings
    if result["warnings"]:
        print("⚠️  Warnings:")
        for warning in result["warnings"]:
            print(f"  - {warning}")
        print()

    # Print status
    if result["status"] == "ok":
        print("✅ Documentation is up-to-date!")
        sys.exit(0)
    elif result["status"] == "warning":
        print("⚠️  Documentation has warnings")
        sys.exit(0)
    else:
        print("❌ Documentation has errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
