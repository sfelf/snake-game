#!/usr/bin/env python3
"""Set up Git hooks for local validation."""

import os
import stat
from pathlib import Path


def remove_legacy_post_commit_hook(
    hooks_dir: Path | None = None,
) -> bool:
    """Remove the obsolete badge hook without touching unrelated user hooks.

    Args:
        hooks_dir: Directory containing the repository's Git hooks.

    Returns:
        True when a legacy managed hook was removed, otherwise False.
    """
    resolved_hooks_dir = hooks_dir or Path(".git/hooks")
    post_commit_hook = resolved_hooks_dir / "post-commit"
    if not post_commit_hook.exists():
        return False

    try:
        hook_content = post_commit_hook.read_text(encoding="utf-8")
    except OSError as error:
        print(f"⚠️  Could not inspect existing {post_commit_hook}: {error}")
        return False

    managed_markers = (
        "scripts/generate_badges.py",
        'git commit -m "Update badges [skip ci]"',
    )
    if not all(marker in hook_content for marker in managed_markers):
        print(f"ℹ️  Preserved unrelated existing hook at {post_commit_hook}")
        return False

    try:
        post_commit_hook.unlink()
    except OSError as error:
        print(f"⚠️  Could not remove legacy {post_commit_hook}: {error}")
        return False

    print(f"✅ Removed legacy badge hook at {post_commit_hook}")
    return True


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
    remove_legacy_post_commit_hook()
    setup_pre_commit_hook()

    print("\n🎉 Git hooks setup complete!")
    print("\n📋 What happens now:")
    print("   • Before each commit: Formatting and tests run")
    print("   • On GitHub: CI runs tests, quality checks, and security scanning")
    print("\n💡 To disable hooks temporarily: git commit --no-verify")

    return 0


if __name__ == "__main__":
    exit(main())
