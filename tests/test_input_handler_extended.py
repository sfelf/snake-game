"""Extended tests for InputHandler to improve coverage."""

from unittest.mock import Mock

import pygame
import pytest

from snake_game.controllers.input_handler import InputHandler
from snake_game.models import Direction, GameState


class TestInputHandlerExtended:
    """Extended test cases for InputHandler."""

    def test_handle_splash_screen_show_reset_confirm(self):
        """Test splash screen input for show reset confirm."""
        handler = InputHandler()

        # Create mock event for 'r' key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_r

        result = handler.handle_event(event, GameState.SPLASH)

        assert result == "show_reset_confirm"

    def test_handle_high_scores_restart_game(self):
        """Test high scores input for restart game."""
        handler = InputHandler()

        # Create mock event for space key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_SPACE

        result = handler.handle_event(event, GameState.HIGH_SCORES)

        assert result == "restart_game"

    def test_handle_high_scores_show_splash(self):
        """Test high scores input for show splash."""
        handler = InputHandler()

        # Create mock event for escape key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = handler.handle_event(event, GameState.HIGH_SCORES)

        assert result == "show_splash"

    def test_handle_high_scores_show_reset_confirm(self):
        """Test high scores input for show reset confirm."""
        handler = InputHandler()

        # Create mock event for 'r' key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_r

        result = handler.handle_event(event, GameState.HIGH_SCORES)

        assert result == "show_reset_confirm"

    def test_handle_high_scores_unknown_key(self):
        """Test high scores input for unknown key."""
        handler = InputHandler()

        # Create mock event for unknown key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a

        result = handler.handle_event(event, GameState.HIGH_SCORES)

        assert result is None

    def test_handle_confirm_reset_confirm(self):
        """Test confirm reset input for confirm."""
        handler = InputHandler()

        # Create mock event for 'y' key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_y

        result = handler.handle_event(event, GameState.CONFIRM_RESET)

        assert result == "confirm_reset"

    def test_handle_confirm_reset_cancel_n(self):
        """Test confirm reset input for cancel with 'n'."""
        handler = InputHandler()

        # Create mock event for 'n' key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_n

        result = handler.handle_event(event, GameState.CONFIRM_RESET)

        assert result == "cancel_reset"

    def test_handle_confirm_reset_cancel_escape(self):
        """Test confirm reset input for cancel with escape."""
        handler = InputHandler()

        # Create mock event for escape key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        result = handler.handle_event(event, GameState.CONFIRM_RESET)

        assert result == "cancel_reset"

    def test_handle_confirm_reset_unknown_key(self):
        """Test confirm reset input for unknown key."""
        handler = InputHandler()

        # Create mock event for unknown key
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_a

        result = handler.handle_event(event, GameState.CONFIRM_RESET)

        assert result is None

    def test_get_direction_from_action_move_up(self):
        """Test get_direction_from_action for move_up."""
        handler = InputHandler()

        result = handler.get_direction_from_action("move_up")

        assert result == Direction.UP

    def test_get_direction_from_action_move_down(self):
        """Test get_direction_from_action for move_down."""
        handler = InputHandler()

        result = handler.get_direction_from_action("move_down")

        assert result == Direction.DOWN

    def test_get_direction_from_action_move_left(self):
        """Test get_direction_from_action for move_left."""
        handler = InputHandler()

        result = handler.get_direction_from_action("move_left")

        assert result == Direction.LEFT

    def test_get_direction_from_action_move_right(self):
        """Test get_direction_from_action for move_right."""
        handler = InputHandler()

        result = handler.get_direction_from_action("move_right")

        assert result == Direction.RIGHT

    def test_get_direction_from_action_invalid(self):
        """Test get_direction_from_action for invalid action."""
        handler = InputHandler()

        result = handler.get_direction_from_action("invalid_action")

        assert result is None

    def test_get_direction_from_action_none(self):
        """Test get_direction_from_action for None action."""
        handler = InputHandler()

        result = handler.get_direction_from_action(None)

        assert result is None
