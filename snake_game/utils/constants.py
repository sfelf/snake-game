"""Constants for the Snake Game."""

from typing import Tuple


class GameConstants:
    """Game constants and configuration."""

    # Grid dimensions
    GRID_WIDTH = 40
    GRID_HEIGHT = 30
    CELL_SIZE = 20

    # UI layout
    BORDER_WIDTH = 2
    UI_HEIGHT = 60

    # Window dimensions
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + (BORDER_WIDTH * 2)
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + (BORDER_WIDTH * 2) + UI_HEIGHT

    # Playing area
    PLAY_AREA_X = BORDER_WIDTH
    PLAY_AREA_Y = BORDER_WIDTH + UI_HEIGHT
    PLAY_AREA_WIDTH = GRID_WIDTH * CELL_SIZE
    PLAY_AREA_HEIGHT = GRID_HEIGHT * CELL_SIZE

    # Game mechanics
    INITIAL_SNAKE_LENGTH = 5
    INITIAL_SPEED = 200  # milliseconds between moves
    SPEED_INCREASE = 10  # speed increase per fruit eaten
    MIN_SPEED = 50  # minimum speed (maximum difficulty)
    POINTS_PER_FRUIT = 4

    # Colors
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    DARK_GREEN: Tuple[int, int, int] = (0, 128, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    LIGHT_GRAY: Tuple[int, int, int] = (200, 200, 200)
    BROWN: Tuple[int, int, int] = (139, 69, 19)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)

    # Audio settings
    AUDIO_FREQUENCY = 22050
    AUDIO_SIZE = -16
    AUDIO_CHANNELS = 2
    AUDIO_BUFFER = 512

    # Game settings
    TARGET_FPS = 60
