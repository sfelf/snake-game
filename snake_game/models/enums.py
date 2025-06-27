"""Enumerations for the Snake Game."""

from enum import Enum


class Direction(Enum):
    """Direction enumeration for snake movement."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameState(Enum):
    """Game state enumeration."""
    SPLASH = "splash"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    HIGH_SCORES = "high_scores"
    CONFIRM_RESET = "confirm_reset"


class FruitType(Enum):
    """Different types of fruits."""
    APPLE = ("apple", (255, 0, 0), (0, 150, 0))  # Red with green stem
    PEAR = ("pear", (255, 255, 0), (0, 150, 0))  # Yellow with green stem
    BANANA = ("banana", (255, 255, 0), (139, 69, 19))  # Yellow with brown tip
    CHERRY = ("cherry", (220, 20, 60), (0, 150, 0))  # Dark red with green stem
    ORANGE = ("orange", (255, 165, 0), (255, 140, 0))  # Orange with darker shade
