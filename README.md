# Snake Game

[![Test Coverage](https://img.shields.io/badge/coverage-39.3%25-red.svg)](htmlcov/index.html)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://pygame.org)
[![Tests](https://img.shields.io/badge/tests-92%20passing-green.svg)](tests/)
[![Lines of Code](https://img.shields.io/badge/lines%20of%20code-3079-blue.svg)](snake_game/)
[![Code Quality](https://img.shields.io/badge/code%20quality-refactored-brightgreen.svg)](README.md#architecture)
[![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/sfelf/snake-game/actions)























































































A classic Snake game implementation using Python and Pygame with enhanced graphics, professional architecture, and comprehensive testing.

## Features

### Core Gameplay
- **Enhanced Splash Screen**: Welcome screen with animated snake graphics and fruit displays
- **Grid-based Gameplay**: 40x30 grid with 20-pixel cells
- **Progressive Difficulty**: Snake speeds up as it grows longer
- **Scoring System**: 4 points per fruit eaten
- **High Score Tracking**: Keeps track of the top 5 highest scores (starts with all zeros)

### Visual Enhancements
- **High-Quality Twemoji Graphics**: Professional emoji images from Twitter's open-source Twemoji library:
  - 🍎 **Apple**: Crisp red apple with green stem and leaf
  - 🍐 **Pear**: Yellow-green pear with natural shape and highlights  
  - 🍌 **Banana**: Curved yellow banana with brown tip and realistic details
  - 🍒 **Cherry**: Twin bright red cherries with green stems
  - 🍊 **Orange**: Textured orange with natural dimpled surface
- **Vector-Quality Rendering**: SVG-converted images provide crisp, emoji-quality graphics
- **Smart Fallback System**: Custom graphics for systems where images can't be loaded
- **Enhanced Snake Graphics**: 
  - Distinct head with directional eyes
  - Patterned body segments with alternating colors
  - Scale texture details
- **Professional UI Layout**:
  - Dedicated UI area showing score, length, and speed
  - Game border separating play area
  - Speed indicator showing current game pace
- **Visual Effects**:
  - Pulsing "Game Over" text
  - Color-coded high score rankings (gold, silver, bronze)
  - Shadow effects on title text

### Audio Features
- **Background Music**: Melodic soundtrack that plays during gameplay
- **Dynamic Sound Effects**: Audio that increases in urgency as the snake grows
- **Contextual Audio**: Different sounds for eating, moving, and game over

### Enhanced Controls & Features
- **Smart Fruit Placement**: Fruits never spawn on the outer edge of the playing area
- **Quit Command**: Press 'Q' to exit the game at any time
- **High Score Reset**: Hidden 'R' command with confirmation dialog to reset scores
- **Improved Navigation**: Enhanced menu system with multiple game states

## Architecture

This project follows professional software development practices with a clean, modular architecture:

### Design Patterns
- **Model-View-Controller (MVC)**: Clear separation of concerns
- **Single Responsibility Principle**: Each class has one focused purpose
- **Dependency Injection**: Components are loosely coupled
- **Observer Pattern**: Game state management

## Architecture

### Code Quality & Testing
- **Test Coverage**: 38.5% and growing with comprehensive test suite
- **Separation of Concerns**: Clean architecture with distinct layers
- **Component-Based Rendering**: Modular rendering system with specialized components
- **Path Smoothing**: Advanced mathematical algorithms for smooth snake curves
- **OOP Best Practices**: Proper encapsulation, inheritance, and polymorphism

### Refactored Architecture
The codebase has been refactored to follow modern software engineering principles:

#### Rendering Components
- **SnakeBodyRenderer**: Handles snake body rendering with proper proportions and 3D effects
- **SnakeHeadRenderer**: Specialized head rendering with realistic features (eyes, tongue, nostrils)
- **SnakeScaleRenderer**: Manages scale patterns and texture details
- **PathSmoother**: Advanced curve generation using Catmull-Rom splines

#### Design Patterns
- **Component Pattern**: Rendering system broken into specialized components
- **Strategy Pattern**: Different rendering strategies for different snake parts
- **Factory Pattern**: Fruit creation and management
- **Observer Pattern**: Game state change notifications

#### Testing Strategy
- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: Cross-component interaction testing
- **Coverage Reporting**: Automated coverage tracking and reporting
- **Continuous Testing**: Test suite runs on every change

### Project Structure

```
snake-game/
├── snake_game/
│   ├── models/              # Game logic and data models
│   │   ├── __init__.py
│   │   ├── enums.py         # Game enumerations
│   │   ├── snake.py         # Snake model
│   │   ├── fruit.py         # Fruit model
│   │   ├── score.py         # Score management
│   │   └── game_state.py    # Game state management
│   ├── views/               # Rendering and visual components
│   │   ├── __init__.py
│   │   ├── renderer.py      # Main game renderer (refactored)
│   │   └── snake_renderer.py # Specialized snake rendering components
│   ├── controllers/         # Game logic coordination
│   │   ├── __init__.py
│   │   ├── game_controller.py    # Main game controller
│   │   └── input_handler.py     # Input processing
│   ├── utils/               # Utilities and helper classes
│   │   ├── __init__.py
│   │   ├── constants.py     # Game constants
│   │   ├── audio.py         # Audio management
│   │   └── path_smoother.py # Advanced curve generation
│   ├── assets/              # Game assets
│   │   └── images/          # High-quality fruit images
│   ├── __init__.py
│   └── main.py              # Entry point
├── tests/                   # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_models.py       # Model tests
│   ├── test_controllers.py  # Controller tests
│   ├── test_utils.py        # Utility tests
│   ├── test_integration.py  # Integration tests
│   ├── test_path_smoother.py # Path smoothing tests
│   ├── test_snake_renderers.py # Component renderer tests
│   └── test_renderer_refactored.py # Refactored renderer tests
├── htmlcov/                 # Coverage HTML reports
├── pytest.ini              # Pytest configuration
├── pyproject.toml           # Poetry configuration with coverage tools
├── poetry.lock              # Dependency lock file
├── coverage.json            # Coverage data
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Key Components

#### Models
- **Snake**: Handles snake movement, collision detection, and growth
- **Fruit**: Manages fruit spawning, types, and collision detection
- **ScoreManager**: Handles scoring and high score persistence
- **GameStateManager**: Manages game state transitions

#### Views
- **GameRenderer**: Handles all rendering and visual effects

#### Controllers
- **GameController**: Main game loop and component coordination
- **InputHandler**: Processes user input and converts to actions

#### Utils
- **GameConstants**: Centralized configuration and constants
- **AudioManager**: Handles all audio functionality

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed.

```bash
# Clone the repository
git clone https://github.com/sfelf/snake-game.git
cd snake-game

# Install dependencies
poetry install
```

## Usage

Run the game using one of these commands:

```bash
# Using the configured script
poetry run snake-game

# Or using the module directly
poetry run python -m snake_game.main
```

## Controls

### Game Controls
- **Arrow Keys**: Control snake direction (Up, Down, Left, Right)
- **Q**: Quit the game at any time

### Menu Navigation
- **Any Key**: Start game from splash screen
- **Space**: Restart game after game over
- **H**: View high scores after game over
- **Escape**: Return to splash screen from high scores
- **R**: Reset high scores (with confirmation)
- **Y/N**: Confirm/cancel high score reset

## Development

### Running Tests

The project includes a comprehensive test suite with coverage reporting:

```bash
# Run all tests
poetry run pytest

# Run tests with coverage report
poetry run pytest --cov=snake_game --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest --cov=snake_game --cov-report=html

# Run specific test file
poetry run pytest tests/test_path_smoother.py

# Run tests with verbose output
poetry run pytest -v
```

### Coverage Reports

- **Current Coverage**: 38.5%
- **HTML Reports**: Available in `htmlcov/index.html` after running coverage
- **JSON Data**: Coverage data stored in `coverage.json`
- **Missing Lines**: Detailed in terminal output with `--cov-report=term-missing`

### Test Categories

- **Unit Tests**: Individual component testing (`test_models.py`, `test_utils.py`)
- **Integration Tests**: Cross-component testing (`test_integration.py`)
- **Component Tests**: Specialized renderer testing (`test_snake_renderers.py`)
- **Architecture Tests**: Refactored system testing (`test_renderer_refactored.py`)

### Running Tests

The project includes a comprehensive test suite using pytest:

```bash
# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v

# Run specific test categories
poetry run pytest tests/test_models.py
poetry run pytest tests/test_controllers.py
poetry run pytest tests/test_integration.py

# Run tests with coverage
poetry run pytest --cov=snake_game
```

### Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Model Tests**: Test game logic and data models
- **Controller Tests**: Test input handling and game coordination
- **Utility Tests**: Test helper functions and constants

### Code Quality

The codebase follows professional standards:

- **Type Hints**: Full type annotation for better IDE support
- **Docstrings**: Comprehensive documentation for all public methods
- **Error Handling**: Graceful handling of edge cases
- **Separation of Concerns**: Clear boundaries between components
- **Testability**: Designed for easy testing and mocking

## Technical Details

### Game Dimensions
- **Grid Size**: 40 columns × 30 rows
- **Cell Size**: 20×20 pixels
- **Play Area**: 800×600 pixels (with border)
- **UI Area**: 60 pixels height for score display
- **Total Window**: 804×662 pixels (including border)

### Gameplay Mechanics
- **Initial Snake Length**: 5 segments
- **Starting Position**: Center of the grid
- **Frame Rate**: 60 FPS
- **Initial Speed**: 200ms between moves
- **Speed Increase**: 10ms faster per fruit eaten (minimum 50ms)
- **Fruit Placement**: Avoids 1-cell border around play area edges

### Graphics & Audio
- **Professional Twemoji Graphics**: High-quality emoji images from Twitter's open-source library
- **Vector-Quality Rendering**: SVG-converted images provide crisp, scalable fruit graphics
- **Emoji-Quality Visuals**: Same professional appearance as system emojis
- **Snake Graphics**: Directional head with eyes, patterned body
- **Background Music**: Generated melodic soundtrack
- **Sound Effects**: Dynamic audio with increasing urgency

## Dependencies

- **Python**: ^3.13
- **pygame**: 2.6.1 (for graphics, sound, and input handling)
- **numpy**: ^2.3.1 (for audio generation and mathematical operations)

### Development Dependencies
- **pytest**: ^8.4.1 (for testing framework)

## High Scores

- High scores start at all zeros for new installations
- Automatically saved to `high_scores.json` in the game directory
- Persist between game sessions
- Can be reset using the hidden 'R' command with confirmation
- Top 5 scores are maintained with color-coded rankings

## Game States

The game includes multiple states for a polished experience:

- **Splash**: Welcome screen with instructions and graphics
- **Playing**: Active gameplay with all mechanics
- **Game Over**: Score display and restart options
- **High Scores**: Leaderboard with ranking colors
- **Confirm Reset**: Safety dialog for score reset

## Contributing

We welcome contributions! The modular architecture makes it easy to:

- Add new fruit types in `models/fruit.py`
- Implement new visual effects in `views/renderer.py`
- Add new game mechanics in the appropriate model
- Extend the test suite with new test cases

### Development Guidelines

1. Follow the existing architecture patterns
2. Add tests for new functionality
3. Use type hints and docstrings
4. Maintain separation of concerns
5. Update documentation as needed

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit and link to the license
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — If you remix or build upon the material, you must distribute your contributions under the same license

See the [LICENSE](LICENSE) file for the full license text or visit [Creative Commons](https://creativecommons.org/licenses/by-nc-sa/4.0/) for more details.
