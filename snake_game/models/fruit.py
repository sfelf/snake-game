"""Fruit model for the Snake Game."""

import random
from typing import List, Tuple

from snake_game.models.enums import FruitType


class Fruit:
    """Represents a fruit in the game."""

    def __init__(self, grid_width: int = 40, grid_height: int = 30):
        """Initialize the fruit.

        Args:
            grid_width: Width of the game grid
            grid_height: Height of the game grid
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position: Tuple[int, int] = (0, 0)
        self.fruit_type = FruitType.APPLE
        self.points_value = 4

    def spawn(self, occupied_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Spawn a new fruit at a random location.

        Args:
            occupied_positions: List of positions that are occupied (snake segments)

        Returns:
            The new fruit position
        """
        while True:
            # Avoid the outer edge (1 cell border inside the playing area)
            x = random.randint(1, self.grid_width - 2)
            y = random.randint(1, self.grid_height - 2)

            if (x, y) not in occupied_positions:
                self.position = (x, y)
                self.fruit_type = random.choice(list(FruitType))
                break

        return self.position

    def is_eaten_by(self, position: Tuple[int, int]) -> bool:
        """Check if the fruit is eaten by something at the given position.

        Args:
            position: Position to check against

        Returns:
            True if the fruit is at the same position
        """
        return self.position == position

    @property
    def name(self) -> str:
        """Get the name of the current fruit type."""
        return self.fruit_type.value[0]

    @property
    def primary_color(self) -> Tuple[int, int, int]:
        """Get the primary color of the current fruit type."""
        return self.fruit_type.value[1]

    @property
    def secondary_color(self) -> Tuple[int, int, int]:
        """Get the secondary color of the current fruit type."""
        return self.fruit_type.value[2]
