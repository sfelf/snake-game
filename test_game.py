#!/usr/bin/env python3
"""Test script for the Snake game."""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snake_game.game import SnakeGame, Direction, GameState, FruitType


def test_game_initialization():
    """Test game initialization."""
    print("Testing game initialization...")
    game = SnakeGame()
    
    # Test initial state
    assert game.state == GameState.SPLASH
    assert game.score == 0
    assert len(game.snake) == game.INITIAL_SNAKE_LENGTH
    assert game.direction == Direction.RIGHT
    assert game.high_scores == [0, 0, 0, 0, 0]  # Should start with all zeros
    
    print("✓ Game initialization test passed!")


def test_snake_movement():
    """Test snake movement logic."""
    print("Testing snake movement...")
    game = SnakeGame()
    
    # Test initial snake position
    initial_head = game.snake[0]
    initial_length = len(game.snake)
    
    # Simulate one move
    game.state = GameState.PLAYING
    game.move_snake()
    
    # Check that snake moved right
    new_head = game.snake[0]
    assert new_head[0] == initial_head[0] + 1
    assert new_head[1] == initial_head[1]
    assert len(game.snake) == initial_length  # Should be same length if no fruit eaten
    
    print("✓ Snake movement test passed!")


def test_fruit_types():
    """Test different fruit types."""
    print("Testing fruit types...")
    game = SnakeGame()
    
    # Test that all fruit types are available
    fruit_names = [fruit.value[0] for fruit in FruitType]
    expected_fruits = ['apple', 'pear', 'banana', 'cherry', 'orange']
    
    for expected in expected_fruits:
        assert expected in fruit_names, f"Missing fruit type: {expected}"
    
    # Test fruit spawning avoids edges
    for _ in range(10):  # Test multiple spawns
        game.spawn_fruit()
        x, y = game.fruit_pos
        assert 1 <= x <= game.GRID_WIDTH - 2, f"Fruit x={x} is on edge"
        assert 1 <= y <= game.GRID_HEIGHT - 2, f"Fruit y={y} is on edge"
    
    print("✓ Fruit types test passed!")


def test_high_scores():
    """Test high score functionality."""
    print("Testing high scores...")
    game = SnakeGame()
    
    # Test initial high scores are all zeros
    assert game.high_scores == [0, 0, 0, 0, 0]
    
    # Test updating high scores
    game.update_high_scores(100)
    game.update_high_scores(50)
    game.update_high_scores(150)
    
    # Check that scores are sorted correctly
    assert game.high_scores[0] == 150
    assert game.high_scores[1] == 100
    assert game.high_scores[2] == 50
    assert game.high_scores[3] == 0
    assert game.high_scores[4] == 0
    
    # Test reset functionality
    game.reset_high_scores()
    assert game.high_scores == [0, 0, 0, 0, 0]
    
    print("✓ High scores test passed!")


def test_game_dimensions():
    """Test game dimensions and UI layout."""
    print("Testing game dimensions...")
    game = SnakeGame()
    
    # Test window dimensions
    expected_width = game.GRID_WIDTH * game.CELL_SIZE + (game.BORDER_WIDTH * 2)
    expected_height = game.GRID_HEIGHT * game.CELL_SIZE + (game.BORDER_WIDTH * 2) + game.UI_HEIGHT
    
    assert game.WINDOW_WIDTH == expected_width
    assert game.WINDOW_HEIGHT == expected_height
    
    # Test playing area
    assert game.PLAY_AREA_X == game.BORDER_WIDTH
    assert game.PLAY_AREA_Y == game.BORDER_WIDTH + game.UI_HEIGHT
    
    print("✓ Game dimensions test passed!")


def main():
    """Run all tests."""
    print("Running Enhanced Snake Game tests...\n")
    
    try:
        test_game_initialization()
        test_snake_movement()
        test_fruit_types()
        test_high_scores()
        test_game_dimensions()
        
        print("\n🎉 All tests passed! The enhanced Snake game is ready to play!")
        print("\nNew features:")
        print("  ✓ Multiple fruit types with custom graphics")
        print("  ✓ Enhanced snake graphics with head/body distinction")
        print("  ✓ UI area with score, length, and speed display")
        print("  ✓ Game border and improved layout")
        print("  ✓ Fruit spawning avoids edges")
        print("  ✓ Quit command (Q key)")
        print("  ✓ High score reset functionality (R key)")
        print("  ✓ Enhanced splash screen with graphics")
        print("\nTo run the game:")
        print("  poetry run snake-game")
        print("  or")
        print("  poetry run python -m snake_game.main")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
