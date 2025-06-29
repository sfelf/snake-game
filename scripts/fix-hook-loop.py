#!/usr/bin/env python3
"""Fix infinite loop caused by Git hooks."""

import subprocess
import sys
from pathlib import Path


def stop_git_processes():
    """Stop any running git processes that might be in a loop."""
    try:
        # Kill any git processes that might be stuck
        subprocess.run(["pkill", "-f", "git"], capture_output=True)
        print("✅ Stopped any running git processes")
    except Exception as e:
        print(f"⚠️  Could not stop git processes: {e}")


def reset_git_state():
    """Reset git to a clean state."""
    try:
        # Reset any staged changes
        subprocess.run(["git", "reset", "HEAD"], capture_output=True, check=False)
        print("✅ Reset staged changes")

        # Clean up any lock files
        git_dir = Path(".git")
        for lock_file in git_dir.glob("*.lock"):
            lock_file.unlink()
            print(f"✅ Removed {lock_file}")

        for lock_file in git_dir.glob("*/*.lock"):
            lock_file.unlink()
            print(f"✅ Removed {lock_file}")

    except Exception as e:
        print(f"⚠️  Error resetting git state: {e}")


def reinstall_hooks():
    """Reinstall the fixed hooks."""
    try:
        subprocess.run(
            ["poetry", "run", "python", "scripts/setup-hooks.py"], check=True
        )
        print("✅ Reinstalled fixed hooks")
    except Exception as e:
        print(f"❌ Error reinstalling hooks: {e}")
        return False
    return True


def main():
    """Main recovery function."""
    print("🔧 Fixing Git hook infinite loop...")

    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("❌ Must be run from project root directory")
        sys.exit(1)

    # Stop any running processes
    stop_git_processes()

    # Reset git state
    reset_git_state()

    # Reinstall hooks with fixes
    if reinstall_hooks():
        print("\n✅ Hook loop fixed!")
        print("\n📋 What was fixed:")
        print("   • Post-commit hook now checks for badge commits to prevent loops")
        print("   • Pre-commit hook skips badge-only commits")
        print("   • Added safeguards against infinite recursion")
        print("\n💡 You can now commit normally without loops")
    else:
        print("\n❌ Could not reinstall hooks automatically")
        print(
            "💡 You may need to manually remove .git/hooks/pre-commit and .git/hooks/post-commit"
        )
        print("   Then run: poetry run python scripts/setup-hooks.py")


if __name__ == "__main__":
    main()
