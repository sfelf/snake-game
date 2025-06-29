"""Input handling for the Snake Game."""

from typing import Optional

import pygame

from ..models import Direction, GameState


class InputHandler:
    """Handles all user input for the game."""

    def __init__(self):
        """Initialize the input handler."""
        pass

    def handle_event(
        self, event: pygame.event.Event, current_state: GameState
    ) -> Optional[str]:
        """Handle a pygame event and return an action.

        Args:
            event: Pygame event to handle
            current_state: Current game state

        Returns:
            Action string or None
        """
        if event.type != pygame.KEYDOWN:
            return None

        # Global quit command
        if event.key == pygame.K_q:
            return "quit"

        # State-specific input handling
        if current_state == GameState.SPLASH:
            return self._handle_splash_input(event)
        elif current_state == GameState.PLAYING:
            return self._handle_playing_input(event)
        elif current_state == GameState.GAME_OVER:
            return self._handle_game_over_input(event)
        elif current_state == GameState.HIGH_SCORES:
            return self._handle_high_scores_input(event)
        elif current_state == GameState.CONFIRM_RESET:
            return self._handle_confirm_reset_input(event)

        return None

    def _handle_splash_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input on the splash screen.

        Args:
            event: Pygame event

        Returns:
            Action string or None
        """
        if event.key == pygame.K_r:
            return "show_reset_confirm"
        else:
            return "start_game"

    def _handle_playing_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input during gameplay.

        Args:
            event: Pygame event

        Returns:
            Action string or None
        """
        if event.key == pygame.K_r:
            return "show_reset_confirm"

        # Direction keys
        direction_map = {
            pygame.K_UP: "move_up",
            pygame.K_DOWN: "move_down",
            pygame.K_LEFT: "move_left",
            pygame.K_RIGHT: "move_right",
        }

        return direction_map.get(event.key)

    def _handle_game_over_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input on the game over screen.

        Args:
            event: Pygame event

        Returns:
            Action string or None
        """
        if event.key == pygame.K_SPACE:
            return "restart_game"
        elif event.key == pygame.K_h:
            return "show_high_scores"
        elif event.key == pygame.K_r:
            return "show_reset_confirm"

        return None

    def _handle_high_scores_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input on the high scores screen.

        Args:
            event: Pygame event

        Returns:
            Action string or None
        """
        if event.key == pygame.K_SPACE:
            return "restart_game"
        elif event.key == pygame.K_ESCAPE:
            return "show_splash"
        elif event.key == pygame.K_r:
            return "show_reset_confirm"

        return None

    def _handle_confirm_reset_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input on the reset confirmation screen.

        Args:
            event: Pygame event

        Returns:
            Action string or None
        """
        if event.key == pygame.K_y:
            return "confirm_reset"
        elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
            return "cancel_reset"

        return None

    def get_direction_from_action(self, action: str) -> Optional[Direction]:
        """Convert an action string to a Direction enum.

        Args:
            action: Action string

        Returns:
            Direction enum or None
        """
        direction_map = {
            "move_up": Direction.UP,
            "move_down": Direction.DOWN,
            "move_left": Direction.LEFT,
            "move_right": Direction.RIGHT,
        }

        return direction_map.get(action)
