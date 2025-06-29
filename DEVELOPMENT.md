# Development Guide

This document provides comprehensive information for developers working on the Snake Game project.

## Automated Badge System

### Overview
The project uses an automated badge system that updates on every commit to keep README badges current with the latest project status.

### Badge Types
- **Coverage**: Test coverage percentage with color coding
- **Python**: Python version requirement
- **Pygame**: Pygame version used
- **Tests**: Number of passing tests
- **Lines of Code**: Total lines of code in the project
- **Code Quality**: Current code quality status
- **License**: Project license (CC BY-NC-SA 4.0 - Non-Commercial)
- **Build Status**: CI/CD pipeline status

### Automation Components

#### 1. Git Hooks
- **Pre-commit Hook**: Runs tests and updates badges before each commit
- **Post-commit Hook**: Commits badge updates if changes were made

#### 2. GitHub Actions
- **CI/CD Pipeline**: Runs on every push and pull request
- **Multi-Python Testing**: Tests against Python 3.8-3.12
- **Coverage Reporting**: Uploads coverage to Codecov
- **Badge Generation**: Updates badges on main branch commits

#### 3. Scripts
- `scripts/generate_badges.py`: Main badge generation script
- `scripts/pre-commit-hook.py`: Pre-commit validation script
- `scripts/setup-hooks.py`: Git hooks installation script

### Setup Instructions

#### Initial Setup
```bash
# Install development dependencies
poetry install

# Setup Git hooks for automated badge updates
poetry run python scripts/setup-hooks.py

# Verify setup by running badge generation
poetry run python scripts/generate_badges.py
```

#### Manual Badge Update
```bash
# Generate badges manually
poetry run python scripts/generate_badges.py

# Run tests and update coverage
poetry run pytest --cov=snake_game --cov-report=json --cov-report=html
```

### Badge Color Coding

#### Coverage Badge
- 🟢 **90%+**: Bright Green
- 🟢 **80-89%**: Green  
- 🟡 **70-79%**: Yellow Green
- 🟡 **60-69%**: Yellow
- 🟠 **50-59%**: Orange
- 🔴 **<50%**: Red

#### Test Count Badge
- 🟢 **100+ tests**: Bright Green
- 🟢 **50-99 tests**: Green
- 🟡 **25-49 tests**: Yellow Green
- 🟡 **10-24 tests**: Yellow
- 🟠 **<10 tests**: Orange

### Workflow

#### Normal Development
1. Make code changes
2. Run tests locally: `poetry run pytest`
3. Commit changes: `git commit -m "Your message"`
4. Pre-commit hook runs automatically:
   - Runs full test suite
   - Updates badges if needed
   - Stages badge updates
5. Push to GitHub: `git push`
6. GitHub Actions runs CI/CD pipeline

#### Disabling Hooks Temporarily
```bash
# Skip pre-commit hook for urgent commits
git commit --no-verify -m "Urgent fix"

# Re-enable by committing normally
git commit -m "Normal commit with hooks"
```

## Testing Strategy

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component interaction
- **Component Tests**: Specialized renderer testing
- **Architecture Tests**: System design validation

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=snake_game --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_path_smoother.py

# Run with verbose output
poetry run pytest -v

# Generate HTML coverage report
poetry run pytest --cov=snake_game --cov-report=html
```

### Coverage Goals
- **Target**: 80%+ overall coverage
- **Current**: 38.5% (growing with each release)
- **New Code**: Should have 90%+ coverage
- **Critical Components**: 95%+ coverage required

## Code Quality Standards

### Automated Tools
The project uses comprehensive code quality tools that run automatically:

- **Black**: Code formatting (88 char line length)
- **isort**: Import organization and sorting
- **flake8**: Linting with multiple plugins (bugbear, tidy-imports, docstrings, comprehensions)
- **mypy**: Static type checking

See [CODE_QUALITY.md](CODE_QUALITY.md) for detailed configuration and usage.

### Running Quality Tools
```bash
# Format and check all code
poetry run python scripts/format-code.py

# Individual tools
poetry run black snake_game tests scripts
poetry run isort snake_game tests scripts
poetry run flake8 snake_game tests scripts
poetry run mypy snake_game
```

### Architecture Principles
- **Separation of Concerns**: Each class has a single responsibility
- **Component-Based Design**: Modular, reusable components
- **Dependency Injection**: Clean component initialization
- **Design Patterns**: Proper use of established patterns

### Code Style
- **PEP 8**: Python style guide compliance
- **Type Hints**: Use type annotations where beneficial
- **Docstrings**: Comprehensive documentation for all public methods
- **Comments**: Explain complex algorithms and business logic

### Testing Requirements
- **New Features**: Must include comprehensive tests
- **Bug Fixes**: Must include regression tests
- **Refactoring**: Must maintain or improve test coverage
- **Performance**: Critical paths must have performance tests

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# Triggers
- Push to main/develop branches
- Pull requests to main
- Manual workflow dispatch

# Jobs
1. Test (Python 3.8-3.12)
2. Lint (Code quality checks)
3. Security (Bandit security scan)
4. Badge Update (On main branch only)
```

### Pipeline Steps
1. **Checkout Code**: Get latest code
2. **Setup Python**: Install Python version matrix
3. **Install Poetry**: Package manager setup
4. **Cache Dependencies**: Speed up builds
5. **Install Dependencies**: Project requirements
6. **Run Tests**: Full test suite with coverage
7. **Upload Coverage**: Send to Codecov
8. **Generate Badges**: Update project badges
9. **Commit Updates**: Auto-commit badge changes

### Status Checks
- ✅ **All Tests Pass**: Required for merge
- ✅ **Coverage Maintained**: No significant drops
- ✅ **Security Scan**: No high-severity issues
- ✅ **Code Quality**: Meets project standards

## Troubleshooting

### Common Issues

#### Badge Generation Fails
```bash
# Check coverage.json exists
ls -la coverage.json

# Regenerate coverage data
poetry run pytest --cov=snake_game --cov-report=json

# Run badge generation manually
poetry run python scripts/generate_badges.py
```

#### Git Hooks Not Working
```bash
# Check hook files exist and are executable
ls -la .git/hooks/pre-commit .git/hooks/post-commit

# Reinstall hooks
poetry run python scripts/setup-hooks.py

# Test hook manually
.git/hooks/pre-commit
```

#### Infinite Loop in Git Hooks
If you encounter an infinite loop with commits (hooks creating commits that trigger more hooks):

```bash
# Use the automated fix script
poetry run python scripts/fix-hook-loop.py

# Or manually fix:
# 1. Stop any running git processes
pkill -f git

# 2. Remove lock files
rm -f .git/*.lock .git/*/*.lock

# 3. Reset staged changes
git reset HEAD

# 4. Reinstall fixed hooks
poetry run python scripts/setup-hooks.py
```

**Root Cause**: The post-commit hook was creating new commits without proper loop detection, causing infinite recursion.

**Fix**: Added safeguards to detect badge update commits and skip hook execution for them.

#### CI/CD Pipeline Failures
1. Check GitHub Actions tab for detailed logs
2. Verify all dependencies are in pyproject.toml
3. Ensure tests pass locally first
4. Check for environment-specific issues

### Getting Help
- **Issues**: Create GitHub issue with detailed description
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check this file and README.md
- **Code Review**: Request review for complex changes

## Release Process

### Version Bumping
1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with new features
3. Run full test suite
4. Create release commit
5. Tag release: `git tag v1.0.0`
6. Push with tags: `git push --tags`

### Badge Updates on Release
- Coverage percentage reflects latest tests
- Version badges update automatically
- Build status shows release pipeline status
- All badges reflect current state

This automated system ensures that project badges always reflect the current state of the codebase, providing accurate information to users and contributors.
