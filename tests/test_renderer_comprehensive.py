"""Comprehensive tests for GameRenderer to improve coverage."""

from unittest.mock import MagicMock, Mock, patch

import pygame
import pytest

from snake_game.models import Direction, Fruit, FruitType, Snake
from snake_game.views.renderer import GameRenderer


class TestGameRendererComprehensive:
    """Comprehensive test cases for GameRenderer."""

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_initialization(self, mock_font):
        """Test GameRenderer initialization."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        renderer = GameRenderer(mock_screen)

        assert renderer.screen == mock_screen
        assert renderer.font == mock_font_instance
        assert renderer.small_font == mock_font_instance
        assert renderer.large_font == mock_font_instance
        assert not renderer._images_loaded
        assert not renderer.use_images

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.os.path.exists")
    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.pygame.transform.scale")
    def test_load_fruit_images_success(
        self, mock_scale, mock_load, mock_exists, mock_font
    ):
        """Test successful fruit image loading."""
        mock_screen = Mock()
        mock_font.return_value = Mock()
        mock_exists.return_value = True
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        renderer = GameRenderer(mock_screen)
        result = renderer.load_fruit_images()

        assert result is True
        assert len(renderer.fruit_images) == len(FruitType)

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_load_fruit_images_no_files(self, mock_exists, mock_font):
        """Test fruit image loading when files don't exist."""
        mock_screen = Mock()
        mock_font.return_value = Mock()
        mock_exists.return_value = False

        renderer = GameRenderer(mock_screen)
        result = renderer.load_fruit_images()

        assert result is False
        assert len(renderer.fruit_images) == 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.os.path.exists")
    @patch("snake_game.views.renderer.pygame.image.load")
    def test_load_fruit_images_load_error(self, mock_load, mock_exists, mock_font):
        """Test fruit image loading with load error."""
        mock_screen = Mock()
        mock_font.return_value = Mock()
        mock_exists.return_value = True
        mock_load.side_effect = pygame.error("Load failed")

        renderer = GameRenderer(mock_screen)
        result = renderer.load_fruit_images()

        assert result is False

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_ensure_images_loaded(self, mock_font):
        """Test _ensure_images_loaded method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)

        with patch.object(
            renderer, "load_fruit_images", return_value=True
        ) as mock_load:
            renderer._ensure_images_loaded()

            mock_load.assert_called_once()
            assert renderer._images_loaded is True
            assert renderer.use_images is True

            # Second call should not load again
            mock_load.reset_mock()
            renderer._ensure_images_loaded()
            mock_load.assert_not_called()

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    def test_render_splash_screen(self, mock_circle, mock_font):
        """Test render_splash_screen method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"), patch.object(
            renderer, "_draw_splash_graphics"
        ):
            renderer.render_splash_screen()

            # Verify screen was filled and text was rendered
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0
            assert mock_screen.blit.call_count > 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.rect")
    def test_render_game_screen(self, mock_rect, mock_font):
        """Test render_game_screen method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Create mock objects
        mock_snake = Mock(spec=Snake)
        mock_snake.body = [(100, 100), (120, 100), (140, 100)]
        mock_snake.segments = [
            (100, 100),
            (120, 100),
            (140, 100),
        ]  # Add segments attribute
        mock_snake.length = 3  # Add length attribute
        mock_snake.direction = Direction.RIGHT

        mock_fruit = Mock(spec=Fruit)
        mock_fruit.position = (200, 200)
        mock_fruit.fruit_type = FruitType.APPLE

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"), patch.object(
            renderer, "_draw_ui"
        ), patch.object(renderer.snake_body_renderer, "draw_body"), patch.object(
            renderer.snake_head_renderer, "draw_head"
        ), patch.object(
            renderer.snake_scale_renderer, "draw_scales"
        ), patch(
            "snake_game.views.renderer.pygame.draw.circle"
        ):
            renderer.render_game_screen(mock_snake, mock_fruit, 100, 5)

            # Verify methods were called
            mock_screen.fill.assert_called()
            renderer._draw_ui.assert_called_once_with(100, mock_snake.length, 5)

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_game_over_screen(self, mock_font):
        """Test render_game_over_screen method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"):
            renderer.render_game_over_screen(150, True)

            # Verify screen was filled and text was rendered
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0
            assert mock_screen.blit.call_count > 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_high_scores_screen(self, mock_font):
        """Test render_high_scores_screen method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)
        high_scores = [100, 90, 80, 70, 60]

        with patch.object(renderer, "_ensure_images_loaded"):
            renderer.render_high_scores_screen(high_scores)

            # Verify screen was filled and text was rendered
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0
            assert mock_screen.blit.call_count > 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_confirm_reset_screen(self, mock_font):
        """Test render_confirm_reset_screen method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"):
            renderer.render_confirm_reset_screen()

            # Verify screen was filled and text was rendered
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0
            assert mock_screen.blit.call_count > 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    def test_draw_splash_graphics(self, mock_circle, mock_font):
        """Test _draw_splash_graphics method with perfect coiled snake image."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"), \
             patch.object(renderer, "_draw_decorative_fruit_custom"), \
             patch("snake_game.views.renderer.os.path.exists", return_value=False), \
             patch.object(renderer, "_draw_custom_snake_logo") as mock_custom_snake:
            
            renderer._draw_splash_graphics()

            # Since image doesn't exist, should fall back to custom snake
            mock_custom_snake.assert_called_once()

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.rect")
    def test_draw_ui(self, mock_rect, mock_font):
        """Test _draw_ui method."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface

        renderer = GameRenderer(mock_screen)
        renderer._draw_ui(150, 8, 5)

        # Verify text was rendered and blitted
        assert mock_font_instance.render.call_count >= 3  # Score, length, speed
        assert mock_screen.blit.call_count >= 3
        mock_rect.assert_called()  # UI background

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    def test_draw_decorative_fruit_custom(self, mock_circle, mock_font):
        """Test _draw_decorative_fruit_custom method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_draw_decorative_apple") as mock_apple:
            renderer._draw_decorative_fruit_custom(100, 100, FruitType.APPLE)
            mock_apple.assert_called_once_with(100, 100)

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    @patch("snake_game.views.renderer.pygame.draw.rect")
    @patch("snake_game.views.renderer.pygame.draw.ellipse")
    def test_draw_decorative_apple(
        self, mock_ellipse, mock_rect, mock_circle, mock_font
    ):
        """Test _draw_decorative_apple method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer._draw_decorative_apple(100, 100)

        # Verify circles, rect, and ellipse were drawn
        assert mock_circle.call_count >= 2  # Apple body circles
        mock_rect.assert_called()  # Stem
        mock_ellipse.assert_called()  # Leaf

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.polygon")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    @patch("snake_game.views.renderer.pygame.draw.line")
    def test_draw_decorative_banana(
        self, mock_line, mock_circle, mock_polygon, mock_font
    ):
        """Test _draw_decorative_banana method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer._draw_decorative_banana(100, 100)

        # Verify polygon, circle, and line were drawn
        mock_polygon.assert_called()  # Banana body
        mock_circle.assert_called()  # Stem
        mock_line.assert_called()  # Banana curve

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    @patch("snake_game.views.renderer.pygame.draw.line")
    def test_draw_decorative_cherry(self, mock_line, mock_circle, mock_font):
        """Test _draw_decorative_cherry method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer._draw_decorative_cherry(100, 100)

        # Verify circles were drawn (two cherries)
        assert mock_circle.call_count >= 4  # Two cherries with outlines
        # Verify stem line was drawn
        mock_line.assert_called()

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    def test_draw_decorative_orange(self, mock_circle, mock_font):
        """Test _draw_decorative_orange method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer._draw_decorative_orange(100, 100)

        # Verify circle was drawn
        mock_circle.assert_called()

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    @patch("snake_game.views.renderer.pygame.draw.ellipse")
    @patch("snake_game.views.renderer.pygame.draw.rect")
    def test_draw_decorative_pear(
        self, mock_rect, mock_ellipse, mock_circle, mock_font
    ):
        """Test _draw_decorative_pear method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer._draw_decorative_pear(100, 100)

        # Verify circles, ellipse, and rect were drawn
        assert mock_circle.call_count >= 2  # Pear body parts
        mock_rect.assert_called()  # Stem

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.pygame.draw.circle")
    @patch("snake_game.views.renderer.pygame.draw.rect")
    @patch("snake_game.views.renderer.pygame.draw.polygon")
    @patch("snake_game.views.renderer.pygame.draw.line")
    @patch("snake_game.views.renderer.pygame.draw.ellipse")
    def test_draw_decorative_fruit_image(
        self, mock_ellipse, mock_line, mock_polygon, mock_rect, mock_circle, mock_font
    ):
        """Test _draw_decorative_fruit_image method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        renderer.use_images = False  # Force fallback to custom drawing

        renderer._draw_decorative_fruit_image(100, 100, FruitType.APPLE)

        # Should fall back to custom drawing
        assert mock_circle.call_count >= 2  # Apple circles
        mock_rect.assert_called()  # Apple stem

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_get_assets_directory(self, mock_font):
        """Test _get_assets_directory method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)
        assets_dir = renderer._get_assets_directory()

        # Should return a string path
        assert isinstance(assets_dir, str)
        assert "assets" in assets_dir

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.os.path.exists")
    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.pygame.transform.scale")
    def test_load_single_fruit_image_success(
        self, mock_scale, mock_load, mock_exists, mock_font
    ):
        """Test _load_single_fruit_image method success."""
        mock_screen = Mock()
        mock_font.return_value = Mock()
        mock_exists.return_value = True
        mock_image = Mock()
        mock_load.return_value = mock_image
        mock_scale.return_value = mock_image

        renderer = GameRenderer(mock_screen)
        result = renderer._load_single_fruit_image("/assets", "apple")

        assert result is True
        # Check that the image was stored with the fruit name as key
        assert "apple" in renderer.fruit_images

    @patch("snake_game.views.renderer.pygame.font.Font")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_load_single_fruit_image_file_not_found(self, mock_exists, mock_font):
        """Test _load_single_fruit_image method when file doesn't exist."""
        mock_screen = Mock()
        mock_font.return_value = Mock()
        mock_exists.return_value = False

        renderer = GameRenderer(mock_screen)
        result = renderer._load_single_fruit_image("/assets", "apple")

        assert result is False

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_handle_image_loading_result(self, mock_font):
        """Test _handle_image_loading_result method."""
        mock_screen = Mock()
        mock_font.return_value = Mock()

        renderer = GameRenderer(mock_screen)

        # Test with some images loaded
        result = renderer._handle_image_loading_result(3)
        assert result is True

        # Test with no images loaded
        result = renderer._handle_image_loading_result(0)
        assert result is False

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_empty_high_scores(self, mock_font):
        """Test render_high_scores_screen with empty scores."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"):
            renderer.render_high_scores_screen([])

            # Should still render header and "No scores" message
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_game_over_not_high_score(self, mock_font):
        """Test render_game_over_screen when not a high score."""
        mock_screen = Mock()
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance

        # Mock text rendering
        mock_surface = Mock()
        mock_font_instance.render.return_value = mock_surface
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 100, 50)

        renderer = GameRenderer(mock_screen)

        with patch.object(renderer, "_ensure_images_loaded"):
            renderer.render_game_over_screen(50, False)

            # Verify different message is shown
            mock_screen.fill.assert_called()
            assert mock_font_instance.render.call_count > 0
