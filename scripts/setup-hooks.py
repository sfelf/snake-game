#!/usr/bin/env python3
"""Setup Git hooks for automated badge updates."""

import os
import shutil
import stat
from pathlib import Path


def setup_pre_commit_hook():
    """Setup pre-commit hook."""
    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(exist_ok=True)

    pre_commit_hook = hooks_dir / "pre-commit"

    # Create the hook script
    hook_content = """#!/bin/bash
# Pre-commit hook to update badges and run tests

# Check if this is a badge update commit to prevent unnecessary work
if git diff --cached --name-only | grep -q "README.md\\|badges/" && git diff --cached --quiet -- . ':!README.md' ':!badges/'; then
    echo "📝 Skipping pre-commit checks (badge-only commit)"
    exit 0
fi

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


def setup_post_commit_hook():
    """Setup post-commit hook for badge updates."""
    hooks_dir = Path(".git/hooks")
    hooks_dir.mkdir(exist_ok=True)

    post_commit_hook = hooks_dir / "post-commit"

    # Create the hook script
    hook_content = """#!/bin/bash
# Post-commit hook to update badges after successful commit

# Check if this is already a badge update commit to prevent infinite loop
if git log -1 --pretty=%B | grep -q "Update badges \\[skip ci\\]"; then
    echo "📝 Skipping badge update (already a badge commit)"
    exit 0
fi

echo "🔄 Updating badges after commit..."

# Generate updated badges
poetry run python scripts/generate_badges.py

# Check if badges were updated
if git diff --quiet README.md badges/; then
    echo "📝 No badge updates needed"
else
    echo "📝 Badges updated, creating follow-up commit..."
    git add README.md badges/
    git commit -m "Update badges [skip ci]" --no-verify
fi
"""

    with open(post_commit_hook, "w") as f:
        f.write(hook_content)

    # Make the hook executable
    st = os.stat(post_commit_hook)
    os.chmod(post_commit_hook, st.st_mode | stat.S_IEXEC)

    print(f"✅ Post-commit hook installed at {post_commit_hook}")


def main():
    """Main setup function."""
    print("🔧 Setting up Git hooks for automated badge updates...")

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
    setup_post_commit_hook()

    print("\n🎉 Git hooks setup complete!")
    print("\n📋 What happens now:")
    print("   • Before each commit: Tests run and badges update")
    print("   • After each commit: Badges are committed if changed")
    print("   • On GitHub: CI/CD pipeline runs with full testing")
    print("\n💡 To disable hooks temporarily: git commit --no-verify")

    return 0


if __name__ == "__main__":
    exit(main())
