"""Pytest configuration and fixtures."""

import pytest
import pygame
import tempfile
import os
from snake_game.models import Snake, Fruit, ScoreManager, GameStateManager
from snake_game.utils import GameConstants


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def snake():
    """Create a snake instance for testing."""
    return Snake(initial_length=5, start_x=20, start_y=15)


@pytest.fixture
def fruit():
    """Create a fruit instance for testing."""
    return Fruit(grid_width=40, grid_height=30)


@pytest.fixture
def temp_scores_file():
    """Create a temporary scores file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    yield temp_file
    # Clean up
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def score_manager(temp_scores_file):
    """Create a score manager instance for testing with temporary file."""
    return ScoreManager(scores_file=temp_scores_file)


@pytest.fixture
def state_manager():
    """Create a game state manager instance for testing."""
    return GameStateManager()
