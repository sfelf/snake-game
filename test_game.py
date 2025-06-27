#!/usr/bin/env python3
"""Test script for the Snake game."""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snake_game.game import SnakeGame, Direction, GameState


def test_game_initialization():
    """Test game initialization."""
    print("Testing game initialization...")
    game = SnakeGame()
    
    # Test initial state
    assert game.state == GameState.SPLASH
    assert game.score == 0
    assert len(game.snake) == game.INITIAL_SNAKE_LENGTH
    assert game.direction == Direction.RIGHT
    
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


def test_high_scores():
    """Test high score functionality."""
    print("Testing high scores...")
    game = SnakeGame()
    
    # Test updating high scores
    game.update_high_scores(100)
    game.update_high_scores(50)
    game.update_high_scores(150)
    
    # Check that scores are sorted correctly
    assert game.high_scores[0] == 150
    assert game.high_scores[1] == 100
    assert game.high_scores[2] == 50
    
    print("✓ High scores test passed!")


def main():
    """Run all tests."""
    print("Running Snake Game tests...\n")
    
    try:
        test_game_initialization()
        test_snake_movement()
        test_high_scores()
        
        print("\n🎉 All tests passed! The Snake game is ready to play!")
        print("\nTo run the game:")
        print("  poetry run snake-game")
        print("  or")
        print("  poetry run python -m snake_game.main")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
