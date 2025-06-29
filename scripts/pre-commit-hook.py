#!/usr/bin/env python3
"""Pre-commit hook to update badges and run tests."""

import subprocess
import sys
import os
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
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False


def main():
    """Main pre-commit hook function."""
    print("🚀 Running pre-commit checks...")
    
    # Ensure we're in the project root
    if not Path('pyproject.toml').exists():
        print("❌ Must be run from project root directory")
        sys.exit(1)
    
    success = True
    
    # Run tests with coverage
    if not run_command('poetry run pytest --cov=snake_game --cov-report=json --cov-report=html -q', 
                      'Running tests with coverage'):
        success = False
    
    # Generate badges
    if not run_command('poetry run python scripts/generate_badges.py', 
                      'Generating badges'):
        success = False
    
    # Check if README was updated
    result = subprocess.run(['git', 'diff', '--name-only', 'README.md'], 
                          capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 README.md badges updated")
        # Stage the updated README
        subprocess.run(['git', 'add', 'README.md', 'badges/'], check=False)
    
    if success:
        print("✅ All pre-commit checks passed!")
        return 0
    else:
        print("❌ Some pre-commit checks failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
