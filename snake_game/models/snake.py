"""Snake model for the Snake Game."""

from typing import List, Tuple

from .enums import Direction


class Snake:
    """Represents the snake in the game."""

    def __init__(self, initial_length: int = 5, start_x: int = 20, start_y: int = 15):
        """Initialize the snake.

        Args:
            initial_length: Starting length of the snake
            start_x: Starting x position
            start_y: Starting y position
        """
        self.segments: List[Tuple[int, int]] = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

        # Initialize snake segments
        for i in range(initial_length):
            self.segments.append((start_x - i, start_y))

    @property
    def head(self) -> Tuple[int, int]:
        """Get the head position of the snake."""
        return self.segments[0] if self.segments else (0, 0)

    @property
    def length(self) -> int:
        """Get the current length of the snake."""
        return len(self.segments)

    def set_direction(self, new_direction: Direction) -> bool:
        """Set the next direction for the snake.

        Args:
            new_direction: The new direction to move

        Returns:
            True if direction was set, False if invalid (opposite direction)
        """
        # Prevent moving in opposite direction
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
            return True
        return False

    def move(self, grow: bool = False) -> Tuple[int, int]:
        """Move the snake one step.

        Args:
            grow: Whether the snake should grow (don't remove tail)

        Returns:
            The new head position
        """
        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.head
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        # Add new head
        self.segments.insert(0, new_head)

        # Remove tail unless growing
        if not grow:
            self.segments.pop()

        return new_head

    def check_self_collision(self) -> bool:
        """Check if the snake has collided with itself.

        Returns:
            True if collision detected
        """
        head = self.head
        return head in self.segments[1:]

    def check_wall_collision(self, grid_width: int, grid_height: int) -> bool:
        """Check if the snake has collided with walls.

        Args:
            grid_width: Width of the game grid
            grid_height: Height of the game grid

        Returns:
            True if collision detected
        """
        head_x, head_y = self.head
        return head_x < 0 or head_x >= grid_width or head_y < 0 or head_y >= grid_height

    def reset(self, initial_length: int = 5, start_x: int = 20, start_y: int = 15):
        """Reset the snake to initial state.

        Args:
            initial_length: Starting length of the snake
            start_x: Starting x position
            start_y: Starting y position
        """
        self.segments.clear()
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

        for i in range(initial_length):
            self.segments.append((start_x - i, start_y))
