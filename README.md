# Snake Game

A classic Snake game implementation using Python and Pygame.

## Features

- **Splash Screen**: Welcome screen with game instructions
- **Grid-based Gameplay**: 40x30 grid with 20-pixel cells (800x600 window)
- **Progressive Difficulty**: Snake speeds up as it grows longer
- **Scoring System**: 4 points per fruit eaten
- **Sound Effects**: Dynamic audio that increases in urgency as the snake grows
- **High Score Tracking**: Keeps track of the top 5 highest scores
- **Smooth Controls**: Arrow key controls with direction buffering

## Game Rules

1. Use arrow keys to control the snake's direction
2. Eat the red fruit to grow longer and score points
3. Each fruit gives 4 points and increases the snake's speed
4. Avoid hitting the walls or the snake's own body
5. Try to achieve a high score!

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

- **Arrow Keys**: Control snake direction (Up, Down, Left, Right)
- **Any Key**: Start game from splash screen
- **Space**: Restart game after game over
- **H**: View high scores after game over
- **Escape**: Return to splash screen from high scores

## Game Screens

1. **Splash Screen**: Shows game title and instructions
2. **Game Screen**: Main gameplay with snake, fruit, and score display
3. **Game Over Screen**: Shows final score and options to restart or view high scores
4. **High Scores Screen**: Displays the top 5 highest scores

## Technical Details

- **Grid Size**: 40 columns × 30 rows
- **Cell Size**: 20×20 pixels
- **Window Size**: 800×600 pixels
- **Initial Snake Length**: 5 segments
- **Starting Position**: Center of the grid
- **Frame Rate**: 60 FPS
- **Initial Speed**: 200ms between moves
- **Speed Increase**: 10ms faster per fruit eaten (minimum 50ms)

## Development

### Running Tests

```bash
poetry run python test_game.py
```

### Project Structure

```
snake-game/
├── snake_game/
│   ├── __init__.py
│   ├── main.py          # Entry point
│   └── game.py          # Main game logic
├── test_game.py         # Test suite
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Dependency lock file
└── README.md           # This file
```

## Dependencies

- **Python**: ^3.13
- **pygame**: 2.6.1 (for graphics and sound)
- **numpy**: ^2.3.1 (for sound generation)

## High Scores

High scores are automatically saved to `high_scores.json` in the game directory and persist between game sessions.

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source and available under the MIT License.
