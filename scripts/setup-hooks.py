#!/usr/bin/env python3
"""Set up Git hooks for local validation."""

import os
import stat
from pathlib import Path


def setup_pre_commit_hook():
    """Setup pre-commit hook."""
    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(exist_ok=True)

    pre_commit_hook = hooks_dir / "pre-commit"

    # Create the hook script
    hook_content = """#!/bin/bash
# Pre-commit hook to run local validation

echo "🔄 Running pre-commit checks..."

# Run the Python pre-commit script
poetry run python scripts/pre-commit-hook.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ Pre-commit checks passed!"
else
    echo "❌ Pre-commit checks failed!"
    echo "💡 Fix the issues above before committing."
fi

exit $exit_code
"""

    with open(pre_commit_hook, "w") as f:
        f.write(hook_content)

    # Make the hook executable
    st = os.stat(pre_commit_hook)
    os.chmod(pre_commit_hook, st.st_mode | stat.S_IEXEC)

    print(f"✅ Pre-commit hook installed at {pre_commit_hook}")


def main():
    """Main setup function."""
    print("🔧 Setting up Git hooks for local validation...")

    # Ensure we're in a git repository
    if not Path(".git").exists():
        print("❌ Not in a Git repository!")
        return 1

    # Ensure scripts directory exists and is executable
    scripts_dir = Path("scripts")
    if not scripts_dir.exists():
        print("❌ Scripts directory not found!")
        return 1

    # Make scripts executable
    for script in scripts_dir.glob("*.py"):
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)

    # Setup hooks
    setup_pre_commit_hook()

    print("\n🎉 Git hooks setup complete!")
    print("\n📋 What happens now:")
    print("   • Before each commit: Formatting and tests run")
    print("   • On GitHub: CI runs tests, quality checks, and security scanning")
    print("\n💡 To disable hooks temporarily: git commit --no-verify")

    return 0


if __name__ == "__main__":
    exit(main())
