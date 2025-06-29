# Code Quality Guide

This document outlines the code quality tools and standards used in the Snake Game project.

## 🛠️ Tools Overview

### **Black** - Code Formatter
- **Purpose**: Automatic code formatting for consistent style
- **Configuration**: 88 character line length, Python 3.8+ compatibility
- **Usage**: `poetry run black snake_game tests scripts`

### **isort** - Import Sorter
- **Purpose**: Organize and sort import statements
- **Configuration**: Black-compatible profile, custom sections
- **Usage**: `poetry run isort snake_game tests scripts`

### **flake8** - Linter
- **Purpose**: Code quality, style checking, and error detection
- **Plugins**: 
  - `flake8-bugbear`: Additional bug and design problem checks
  - `flake8-tidy-imports`: Import organization and relative import banning
  - `flake8-docstrings`: Docstring style checking
  - `flake8-comprehensions`: List/dict comprehension improvements
- **Usage**: `poetry run flake8 snake_game tests scripts`

### **mypy** - Type Checker
- **Purpose**: Static type checking for better code reliability
- **Configuration**: Gradual typing approach, strict equality checks
- **Usage**: `poetry run mypy snake_game`

## ⚙️ Configuration

### Black Configuration (`pyproject.toml`)
```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
```

### isort Configuration (`pyproject.toml`)
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["snake_game"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

### flake8 Configuration (`.flake8`)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203,E266,E501,W503
select = B,C,E,F,I,W,T4,B9,D,TI
max-complexity = 12
```

### mypy Configuration (`pyproject.toml`)
```toml
[tool.mypy]
python_version = "3.8"
check_untyped_defs = true
warn_redundant_casts = true
warn_unused_ignores = true
```

## 🚀 Usage

### Manual Formatting
```bash
# Format all code
poetry run python scripts/format-code.py

# Individual tools
poetry run isort snake_game tests scripts
poetry run black snake_game tests scripts
poetry run flake8 snake_game tests scripts
poetry run mypy snake_game
```

### Automated Integration

#### Pre-commit Hooks
- **Automatic**: Runs on every `git commit`
- **Tools**: isort → black → flake8 → tests → badges
- **Auto-staging**: Formatting changes are automatically staged

#### GitHub Actions
- **Triggers**: Push to main/develop, pull requests
- **Checks**: All formatting tools run in CI/CD pipeline
- **Requirements**: All checks must pass for merge

## 📋 Code Standards

### Import Organization
```python
# Standard library imports
import sys
from pathlib import Path

# Third-party imports
import pygame
import numpy as np

# First-party imports
from snake_game.models import Snake, Fruit
from snake_game.utils import GameConstants
```

### Relative Imports Policy
- **❌ Banned**: Relative imports are not allowed
- **✅ Required**: Use absolute imports from package root
- **Example**: Use `from snake_game.models import Snake` not `from .models import Snake`

### Line Length
- **Standard**: 88 characters (Black default)
- **Rationale**: Good balance between readability and screen usage

### Docstring Style
- **Convention**: Google style docstrings
- **Required**: All public functions, classes, and modules
- **Example**:
```python
def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points.
    
    Args:
        point1: First point coordinates (x, y)
        point2: Second point coordinates (x, y)
        
    Returns:
        Distance between the points as a float
        
    Example:
        >>> calculate_distance((0, 0), (3, 4))
        5.0
    """
```

## 🔧 Development Workflow

### 1. Before Committing
```bash
# Format code
poetry run python scripts/format-code.py

# Run tests
poetry run pytest

# Check everything
git commit -m "Your message"  # Pre-commit hooks run automatically
```

### 2. Fixing Issues

#### Import Issues
```bash
# Fix import sorting
poetry run isort snake_game tests scripts --diff  # Preview changes
poetry run isort snake_game tests scripts         # Apply changes
```

#### Formatting Issues
```bash
# Fix code formatting
poetry run black snake_game tests scripts --diff  # Preview changes
poetry run black snake_game tests scripts         # Apply changes
```

#### Linting Issues
```bash
# Check specific issues
poetry run flake8 snake_game --show-source

# Common fixes:
# - Add docstrings to public functions
# - Remove unused imports
# - Fix line length (handled by black)
# - Simplify complex functions
```

#### Type Issues
```bash
# Check type issues
poetry run mypy snake_game --show-error-codes

# Common fixes:
# - Add type hints to function signatures
# - Handle Optional types properly
# - Import types from typing module
```

## 📊 Quality Metrics

### Current Status
- **Coverage**: 39.3% (target: 80%+)
- **Lines of Code**: ~3,079
- **Complexity**: Max 12 (flake8 limit)
- **Type Coverage**: Gradual improvement

### Quality Gates
- ✅ **All tests pass**: Required for commit
- ✅ **Code formatted**: Auto-fixed by pre-commit
- ⚠️ **Linting clean**: Warnings allowed, errors blocked
- ⚠️ **Type hints**: Gradual improvement, not blocking

## 🎯 Best Practices

### Code Organization
```python
# Good: Clear, single responsibility
class SnakeRenderer:
    def draw_head(self, position: Tuple[int, int]) -> None:
        """Draw snake head at given position."""
        
# Bad: Multiple responsibilities
class SnakeEverything:
    def do_all_snake_things(self, *args) -> Any:
        """Does everything snake-related."""
```

### Error Handling
```python
# Good: Specific exception handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return default_value

# Bad: Bare except
try:
    result = risky_operation()
except:
    pass
```

### Type Hints
```python
# Good: Clear type information
def process_coordinates(points: List[Tuple[int, int]]) -> Dict[str, int]:
    """Process coordinate points and return statistics."""
    
# Bad: No type information
def process_coordinates(points):
    """Process coordinate points and return statistics."""
```

## 🔄 Continuous Improvement

### Monthly Reviews
- Review flake8 ignore list and reduce exceptions
- Increase type hint coverage
- Update tool versions and configurations
- Analyze code complexity metrics

### Tool Updates
```bash
# Update tools
poetry update black isort flake8 mypy

# Check for new plugins
poetry search flake8-

# Update configurations as needed
```

### Team Standards
- All new code must pass strict linting
- Existing code improved incrementally
- Documentation updated with code changes
- Regular tool configuration reviews

This comprehensive code quality setup ensures consistent, maintainable, and professional code throughout the Snake Game project! 🐍✨
