"""Tests for local Git hook setup."""

import importlib.util
from pathlib import Path
from unittest.mock import patch

SETUP_HOOKS_PATH = Path(__file__).parents[1] / "scripts" / "setup-hooks.py"
SETUP_HOOKS_SPEC = importlib.util.spec_from_file_location(
    "setup_hooks", SETUP_HOOKS_PATH
)
assert SETUP_HOOKS_SPEC is not None
assert SETUP_HOOKS_SPEC.loader is not None
setup_hooks = importlib.util.module_from_spec(SETUP_HOOKS_SPEC)
SETUP_HOOKS_SPEC.loader.exec_module(setup_hooks)
remove_legacy_post_commit_hook = setup_hooks.remove_legacy_post_commit_hook

LEGACY_HOOK = """#!/bin/bash
poetry run python scripts/generate_badges.py
git commit -m "Update badges [skip ci]" --no-verify
"""


def test_remove_legacy_post_commit_hook_when_absent(tmp_path: Path):
    """Do nothing when no post-commit hook exists."""
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()

    assert remove_legacy_post_commit_hook(hooks_dir) is False


def test_remove_legacy_post_commit_hook_removes_managed_hook(tmp_path: Path):
    """Remove a post-commit hook installed by the old badge setup."""
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()
    post_commit_hook = hooks_dir / "post-commit"
    post_commit_hook.write_text(LEGACY_HOOK, encoding="utf-8")

    assert remove_legacy_post_commit_hook(hooks_dir) is True
    assert not post_commit_hook.exists()


def test_remove_legacy_post_commit_hook_preserves_unrelated_hook(tmp_path: Path):
    """Preserve a post-commit hook not owned by this project."""
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()
    post_commit_hook = hooks_dir / "post-commit"
    user_hook = "#!/bin/bash\nrun-my-custom-hook\n"
    post_commit_hook.write_text(user_hook, encoding="utf-8")

    assert remove_legacy_post_commit_hook(hooks_dir) is False
    assert post_commit_hook.read_text(encoding="utf-8") == user_hook


def test_remove_legacy_post_commit_hook_preserves_unreadable_hook(tmp_path: Path):
    """Preserve an existing hook when its ownership cannot be established."""
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir()
    post_commit_hook = hooks_dir / "post-commit"
    post_commit_hook.write_text(LEGACY_HOOK, encoding="utf-8")

    with patch.object(Path, "read_text", side_effect=OSError("not readable")):
        assert remove_legacy_post_commit_hook(hooks_dir) is False

    assert post_commit_hook.exists()
