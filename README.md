# Snake Game

A classic Snake game implementation using Python and Pygame with enhanced graphics and features.

## Features

### Core Gameplay
- **Enhanced Splash Screen**: Welcome screen with animated snake graphics and fruit displays
- **Grid-based Gameplay**: 40x30 grid with 20-pixel cells
- **Progressive Difficulty**: Snake speeds up as it grows longer
- **Scoring System**: 4 points per fruit eaten
- **High Score Tracking**: Keeps track of the top 5 highest scores (starts with all zeros)

### Visual Enhancements
- **Multiple Fruit Types**: 5 different fruits with unique graphics:
  - 🍎 **Apple**: Red with green stem
  - 🍐 **Pear**: Yellow pear shape with stem
  - 🍌 **Banana**: Curved yellow banana with brown tip
  - 🍒 **Cherry**: Twin red cherries with stems
  - 🍊 **Orange**: Orange with textured surface
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

## Game Rules

1. Use arrow keys to control the snake's direction
2. Eat different types of fruits to grow longer and score points
3. Each fruit gives 4 points and increases the snake's speed
4. Avoid hitting the walls or the snake's own body
5. Try to achieve a high score with the various fruit types!

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

## Game Screens

1. **Splash Screen**: Animated title with decorative snake and fruits, game instructions
2. **Game Screen**: Main gameplay with enhanced graphics, UI panel, and bordered play area
3. **Game Over Screen**: Shows final score with pulsing effects and menu options
4. **High Scores Screen**: Displays top 5 scores with ranking colors
5. **Confirmation Screen**: High score reset confirmation dialog

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
- **Fruit Graphics**: Custom-drawn sprites for each fruit type
- **Snake Graphics**: Directional head with eyes, patterned body
- **Background Music**: Generated melodic soundtrack
- **Sound Effects**: Dynamic audio with increasing urgency

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
│   └── game.py          # Main game logic with enhanced features
├── test_game.py         # Comprehensive test suite
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Dependency lock file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **Python**: ^3.13
- **pygame**: 2.6.1 (for graphics, sound, and input handling)
- **numpy**: ^2.3.1 (for audio generation and mathematical operations)

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

Feel free to contribute to this project by:
- Reporting bugs or issues
- Suggesting new features or improvements
- Submitting pull requests
- Improving documentation
- Adding new fruit types or visual effects

## License

This project is open source and available under the MIT License.
