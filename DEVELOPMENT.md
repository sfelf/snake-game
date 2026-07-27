# Development Guide

This document provides comprehensive information for developers working on the Snake Game project.

## CI Status Badges

### Overview
The README uses live GitHub Actions and Codecov badges. CI does not modify the
repository or create follow-up badge commits.

### Badge Types
- **CI**: Current GitHub Actions workflow status
- **Coverage**: Current Codecov result
- **Python**: Python version requirement
- **Pygame**: Pygame version used
- **License**: Project license (CC BY-NC-SA 4.0 - Non-Commercial)

### Automation Components

#### 1. Git Hooks
- **Pre-commit Hook**: Formats code, runs lint checks, and runs tests
- **Post-commit Hook**: Not installed; commits are never generated automatically

#### 2. GitHub Actions
- **CI Pipeline**: Runs on every push and pull request
- **Python Testing**: Tests against the supported Python 3.13 runtime
- **Coverage Reporting**: Uploads coverage to Codecov
- **Quality Checks**: Enforces Black, isort, flake8, and mypy
- **Security Scanning**: Enforces Bandit medium/high severity findings

#### 3. Scripts
- `scripts/pre-commit-hook.py`: Pre-commit validation script
- `scripts/setup-hooks.py`: Git hooks installation script

### Setup Instructions

#### Initial Setup
```bash
# Install development dependencies
poetry install

# Set up the local validation hook
poetry run python scripts/setup-hooks.py
```

Badge state is derived from the external services and requires no manual update.

### Workflow

#### Normal Development
1. Make code changes
2. Run tests locally: `poetry run pytest`
3. Commit changes: `git commit -m "Your message"`
4. Pre-commit hook runs automatically:
   - Formats imports and Python code
   - Runs flake8
   - Runs full test suite
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
- **Required**: 85%+ overall coverage
- **Current**: 85.7%
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
1. Test (Python 3.13 with coverage)
2. Code quality (Black, isort, flake8, and mypy)
3. Security (Bandit security scan)
```

### Pipeline Steps
1. **Checkout Code**: Get latest code
2. **Setup Python**: Install Python 3.13
3. **Install Poetry**: Install the pinned package manager version
4. **Cache Dependencies**: Speed up builds
5. **Install Dependencies**: Project requirements
6. **Run Tests**: Full test suite with coverage
7. **Upload Coverage**: Send to Codecov
8. **Upload Artifacts**: Retain coverage reports for inspection

### Status Checks
- ✅ **All Tests Pass**: Required for merge
- ✅ **Coverage Maintained**: No significant drops
- ✅ **Security Scan**: No medium- or high-severity issues
- ✅ **Code Quality**: Meets project standards

## Troubleshooting

### Common Issues

#### Git Hooks Not Working
```bash
# Check hook files exist and are executable
ls -la .git/hooks/pre-commit

# Reinstall hooks
poetry run python scripts/setup-hooks.py

# Test hook manually
.git/hooks/pre-commit
```

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
