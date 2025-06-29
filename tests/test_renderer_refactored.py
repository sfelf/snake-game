"""Tests for the refactored game renderer."""

from unittest.mock import MagicMock, Mock, patch

import pygame
import pytest

from snake_game.models import Direction, Snake
from snake_game.views.renderer import GameRenderer


class TestGameRendererRefactored:
    """Test cases for the refactored GameRenderer class."""

    @pytest.fixture
    def mock_screen(self):
        """Create a mock pygame surface."""
        return Mock(spec=pygame.Surface)

    @pytest.fixture
    def renderer(self, mock_screen):
        """Create a GameRenderer instance with mocked components."""
        with patch("pygame.font.Font"):
            with patch.object(GameRenderer, "_ensure_images_loaded"):
                renderer = GameRenderer(mock_screen)

                # Mock the component renderers
                renderer.snake_body_renderer = Mock()
                renderer.snake_head_renderer = Mock()
                renderer.snake_scale_renderer = Mock()

                return renderer

    def test_init_creates_component_renderers(self, mock_screen):
        """Test that initialization creates component renderers."""
        with patch("pygame.font.Font"):
            with patch.object(GameRenderer, "_ensure_images_loaded"):
                renderer = GameRenderer(mock_screen)

                # Should have component renderers
                assert hasattr(renderer, "snake_body_renderer")
                assert hasattr(renderer, "snake_head_renderer")
                assert hasattr(renderer, "snake_scale_renderer")

    def test_draw_snake_single_segment(self, renderer):
        """Test drawing snake with single segment (head only)."""
        snake = Mock()
        snake.segments = [(5, 5)]
        snake.direction = Direction.RIGHT

        renderer._draw_snake(snake)

        # Should only draw head
        renderer.snake_head_renderer.draw_head.assert_called_once_with(
            5, 5, Direction.RIGHT
        )
        renderer.snake_body_renderer.draw_body.assert_not_called()
        renderer.snake_scale_renderer.draw_scales.assert_not_called()

    @patch(
        "snake_game.utils.path_smoother.PathSmoother.convert_segments_to_screen_points"
    )
    @patch("snake_game.utils.path_smoother.PathSmoother.create_smooth_path")
    def test_draw_snake_multiple_segments(
        self, mock_smooth_path, mock_convert, renderer
    ):
        """Test drawing snake with multiple segments."""
        snake = Mock()
        snake.segments = [(5, 5), (4, 5), (3, 5)]
        snake.direction = Direction.RIGHT

        mock_screen_points = [(100, 100), (80, 100), (60, 100)]
        mock_smooth_points = [(100, 100), (90, 100), (80, 100), (70, 100), (60, 100)]

        mock_convert.return_value = mock_screen_points
        mock_smooth_path.return_value = mock_smooth_points

        renderer._draw_snake(snake)

        # Should convert segments to screen points
        mock_convert.assert_called_once_with(snake.segments)

        # Should create smooth path
        mock_smooth_path.assert_called_once_with(mock_screen_points)

        # Should draw body, scales, and head
        renderer.snake_body_renderer.draw_body.assert_called_once_with(
            mock_smooth_points, snake.segments
        )
        renderer.snake_scale_renderer.draw_scales.assert_called_once_with(
            mock_smooth_points
        )
        renderer.snake_head_renderer.draw_head.assert_called_once_with(
            5, 5, Direction.RIGHT
        )

    def test_draw_snake_empty_segments(self, renderer):
        """Test drawing snake with no segments."""
        snake = Mock()
        snake.segments = []
        snake.direction = Direction.RIGHT

        renderer._draw_snake(snake)

        # Should not call any drawing methods
        renderer.snake_head_renderer.draw_head.assert_not_called()
        renderer.snake_body_renderer.draw_body.assert_not_called()
        renderer.snake_scale_renderer.draw_scales.assert_not_called()

    def test_component_renderer_integration(self, mock_screen):
        """Test that component renderers are properly integrated."""
        with patch("pygame.font.Font"):
            with patch.object(GameRenderer, "_ensure_images_loaded"):
                renderer = GameRenderer(mock_screen)

                # Component renderers should be initialized with the screen
                from snake_game.views.snake_renderer import (
                    SnakeBodyRenderer,
                    SnakeHeadRenderer,
                    SnakeScaleRenderer,
                )

                assert isinstance(renderer.snake_body_renderer, SnakeBodyRenderer)
                assert isinstance(renderer.snake_head_renderer, SnakeHeadRenderer)
                assert isinstance(renderer.snake_scale_renderer, SnakeScaleRenderer)

                # All should have the same screen reference
                assert renderer.snake_body_renderer.screen == mock_screen
                assert renderer.snake_head_renderer.screen == mock_screen
                assert renderer.snake_scale_renderer.screen == mock_screen

    def test_separation_of_concerns(self, renderer):
        """Test that rendering concerns are properly separated."""
        snake = Mock()
        snake.segments = [(5, 5), (4, 5), (3, 5)]
        snake.direction = Direction.RIGHT

        with patch(
            "snake_game.utils.path_smoother.PathSmoother.convert_segments_to_screen_points"
        ) as mock_convert:
            with patch(
                "snake_game.utils.path_smoother.PathSmoother.create_smooth_path"
            ) as mock_smooth:
                mock_convert.return_value = [(100, 100), (80, 100), (60, 100)]
                mock_smooth.return_value = [
                    (100, 100),
                    (90, 100),
                    (80, 100),
                    (70, 100),
                    (60, 100),
                ]

                renderer._draw_snake(snake)

                # Each component should handle its own responsibility
                assert renderer.snake_body_renderer.draw_body.called
                assert renderer.snake_scale_renderer.draw_scales.called
                assert renderer.snake_head_renderer.draw_head.called

                # Path smoothing should be handled by utility class
                assert mock_convert.called
                assert mock_smooth.called
