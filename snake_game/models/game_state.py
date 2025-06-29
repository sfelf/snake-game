"""Game state management for the Snake Game."""

from .enums import GameState


class GameStateManager:
    """Manages the current state of the game."""

    def __init__(self, initial_state: GameState = GameState.SPLASH):
        """Initialize the game state manager.

        Args:
            initial_state: The initial game state
        """
        self._current_state = initial_state
        self._previous_state = None

    @property
    def current_state(self) -> GameState:
        """Get the current game state."""
        return self._current_state

    @property
    def previous_state(self) -> GameState:
        """Get the previous game state."""
        return self._previous_state

    def set_state(self, new_state: GameState):
        """Set a new game state.

        Args:
            new_state: The new state to set
        """
        if new_state != self._current_state:
            self._previous_state = self._current_state
            self._current_state = new_state

    def is_state(self, state: GameState) -> bool:
        """Check if the current state matches the given state.

        Args:
            state: State to check against

        Returns:
            True if current state matches
        """
        return self._current_state == state

    def was_state(self, state: GameState) -> bool:
        """Check if the previous state matches the given state.

        Args:
            state: State to check against

        Returns:
            True if previous state matches
        """
        return self._previous_state == state

    def reset(self):
        """Reset to the initial splash state."""
        self._previous_state = self._current_state
        self._current_state = GameState.SPLASH
