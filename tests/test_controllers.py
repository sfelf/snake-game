"""Tests for game controllers."""

from unittest.mock import Mock, patch

import pygame
import pytest

from snake_game.controllers import InputHandler
from snake_game.models import Direction, GameState


class TestInputHandler:
    """Test cases for the InputHandler."""

    def setup_method(self):
        """Set up test fixtures."""
        self.input_handler = InputHandler()

    def test_quit_command(self):
        """Test global quit command."""
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_q

        result = self.input_handler.handle_event(event, GameState.SPLASH)
        assert result == "quit"

        result = self.input_handler.handle_event(event, GameState.PLAYING)
        assert result == "quit"

    def test_non_keydown_event(self):
        """Test that non-keydown events return None."""
        event = Mock()
        event.type = pygame.KEYUP

        result = self.input_handler.handle_event(event, GameState.SPLASH)
        assert result is None

    def test_splash_screen_input(self):
        """Test input handling on splash screen."""
        # Test reset command
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_r

        result = self.input_handler.handle_event(event, GameState.SPLASH)
        assert result == "show_reset_confirm"

        # Test any other key starts game
        event.key = pygame.K_SPACE
        result = self.input_handler.handle_event(event, GameState.SPLASH)
        assert result == "start_game"

        event.key = pygame.K_RETURN
        result = self.input_handler.handle_event(event, GameState.SPLASH)
        assert result == "start_game"

    def test_playing_input(self):
        """Test input handling during gameplay."""
        # Test direction keys
        direction_tests = [
            (pygame.K_UP, "move_up"),
            (pygame.K_DOWN, "move_down"),
            (pygame.K_LEFT, "move_left"),
            (pygame.K_RIGHT, "move_right"),
        ]

        for key, expected_action in direction_tests:
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = key

            result = self.input_handler.handle_event(event, GameState.PLAYING)
            assert result == expected_action

        # Test reset command
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_r

        result = self.input_handler.handle_event(event, GameState.PLAYING)
        assert result == "show_reset_confirm"

    def test_game_over_input(self):
        """Test input handling on game over screen."""
        test_cases = [
            (pygame.K_SPACE, "restart_game"),
            (pygame.K_h, "show_high_scores"),
            (pygame.K_r, "show_reset_confirm"),
        ]

        for key, expected_action in test_cases:
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = key

            result = self.input_handler.handle_event(event, GameState.GAME_OVER)
            assert result == expected_action

    def test_high_scores_input(self):
        """Test input handling on high scores screen."""
        test_cases = [
            (pygame.K_SPACE, "restart_game"),
            (pygame.K_ESCAPE, "show_splash"),
            (pygame.K_r, "show_reset_confirm"),
        ]

        for key, expected_action in test_cases:
            event = Mock()
            event.type = pygame.KEYDOWN
            event.key = key

            result = self.input_handler.handle_event(event, GameState.HIGH_SCORES)
            assert result == expected_action

    def test_confirm_reset_input(self):
        """Test input handling on reset confirmation screen."""
        # Test confirm
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_y

        result = self.input_handler.handle_event(event, GameState.CONFIRM_RESET)
        assert result == "confirm_reset"

        # Test cancel
        cancel_keys = [pygame.K_n, pygame.K_ESCAPE]
        for key in cancel_keys:
            event.key = key
            result = self.input_handler.handle_event(event, GameState.CONFIRM_RESET)
            assert result == "cancel_reset"

    def test_get_direction_from_action(self):
        """Test converting action strings to Direction enums."""
        test_cases = [
            ("move_up", Direction.UP),
            ("move_down", Direction.DOWN),
            ("move_left", Direction.LEFT),
            ("move_right", Direction.RIGHT),
            ("invalid_action", None),
        ]

        for action, expected_direction in test_cases:
            result = self.input_handler.get_direction_from_action(action)
            assert result == expected_direction
