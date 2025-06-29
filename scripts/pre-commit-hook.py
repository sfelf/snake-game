#!/usr/bin/env python3
"""Pre-commit hook to format code, update badges and run tests."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            if result.stderr.strip():
                print(result.stderr)
            if result.stdout.strip():
                print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def main():
    """Main pre-commit hook function."""
    print("🚀 Running pre-commit checks...")

    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("❌ Must be run from project root directory")
        sys.exit(1)

    success = True

    # Format imports with isort
    if not run_command(
        "poetry run isort snake_game tests scripts", "Formatting imports with isort"
    ):
        success = False

    # Format code with black
    if not run_command(
        "poetry run black snake_game tests scripts", "Formatting code with black"
    ):
        success = False

    # Run flake8 linting (lenient for now)
    print("🔍 Running flake8 linting (lenient mode)...")
    run_command(
        "poetry run flake8 snake_game --max-line-length=88 --extend-ignore=E203,E266,E501,W503,D100,D101,D102,D103,D104,TI100 --select=B,C,E,F,I,W,T4,B9",
        "Linting with flake8 (lenient mode)",
    )
    # Don't fail commit on linting issues for now

    # Run tests with coverage
    if not run_command(
        "poetry run pytest --cov=snake_game --cov-report=json --cov-report=html -q",
        "Running tests with coverage",
    ):
        success = False

    # Generate badges
    if not run_command(
        "poetry run python scripts/generate_badges.py", "Generating badges"
    ):
        success = False

    # Check if any files were modified by formatting
    result = subprocess.run(
        ["git", "diff", "--name-only"], capture_output=True, text=True
    )
    if result.stdout.strip():
        print("📝 Code formatting made changes to:")
        for file in result.stdout.strip().split("\n"):
            print(f"   - {file}")
        print("💡 Please review and stage the formatting changes")

        # Auto-stage formatting changes
        subprocess.run(["git", "add", "-u"], check=False)
        print("✅ Automatically staged formatting changes")

    # Check if README was updated
    result = subprocess.run(
        ["git", "diff", "--name-only", "README.md"], capture_output=True, text=True
    )
    if result.stdout.strip():
        print("📝 README.md badges updated")
        # Stage the updated README
        subprocess.run(["git", "add", "README.md", "badges/"], check=False)

    if success:
        print("✅ All pre-commit checks passed!")
        return 0
    else:
        print("❌ Some pre-commit checks failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
