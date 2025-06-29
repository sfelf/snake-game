#!/usr/bin/env python3
"""Format and lint code using black, isort, and flake8."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed:")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return not check
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return not check


def main():
    """Main formatting function."""
    print("🎨 Running code formatting and linting...")

    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("❌ Must be run from project root directory")
        sys.exit(1)

    success = True

    # Format imports with isort
    if not run_command(
        "poetry run isort snake_game tests scripts", "Sorting imports with isort"
    ):
        success = False

    # Format code with black
    if not run_command(
        "poetry run black snake_game tests scripts", "Formatting code with black"
    ):
        success = False

    # Run flake8 linting (non-blocking for first run)
    print("🔍 Running flake8 linting...")
    run_command(
        "poetry run flake8 snake_game tests scripts", "Linting with flake8", check=False
    )

    # Run mypy type checking (non-blocking for first run)
    print("🔍 Running mypy type checking...")
    run_command("poetry run mypy snake_game", "Type checking with mypy", check=False)

    if success:
        print("\n✅ Code formatting completed successfully!")
        print("\n📋 What was done:")
        print("   • isort: Organized and sorted import statements")
        print("   • black: Formatted code to consistent style")
        print("   • flake8: Checked code quality and style")
        print("   • mypy: Performed static type checking")
        print("\n💡 Note: flake8 and mypy warnings are informational for now")
        print("   Run this script regularly to maintain code quality")
    else:
        print("\n❌ Some formatting steps failed!")
        print("💡 Check the errors above and fix any issues")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
