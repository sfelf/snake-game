#!/usr/bin/env python3
"""Tests for splash screen functionality with perfect coiled snake image."""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame

from snake_game.views.renderer import GameRenderer
from snake_game.models.enums import FruitType


class TestSplashScreenWithCoiledSnake:
    """Test splash screen functionality with the perfect coiled snake image."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_screen = Mock()
        self.renderer = GameRenderer(self.mock_screen)

    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_draw_splash_graphics_with_perfect_snake_image(self, mock_exists, mock_load):
        """Test _draw_splash_graphics loads and displays the perfect coiled snake image."""
        # Mock that the perfect snake image exists
        mock_exists.return_value = True
        
        # Mock the loaded image
        mock_snake_image = Mock()
        mock_snake_image.convert_alpha.return_value = mock_snake_image
        mock_load.return_value = mock_snake_image
        
        # Mock pygame.transform.scale
        with patch("snake_game.views.renderer.pygame.transform.scale") as mock_scale:
            mock_scaled_image = Mock()
            mock_scaled_image.get_rect.return_value = Mock(center=(400, 100))
            mock_scale.return_value = mock_scaled_image
            
            with patch.object(self.renderer, "_ensure_images_loaded"), \
                 patch.object(self.renderer, "_draw_decorative_fruit_image"):
                
                self.renderer._draw_splash_graphics()
                
                # Verify the perfect snake image was loaded
                expected_path = os.path.join(
                    self.renderer._get_assets_directory(), 
                    "perfect_coiled_snake_large.png"
                )
                mock_exists.assert_called_with(expected_path)
                mock_load.assert_called_with(expected_path)
                
                # Verify image was scaled to 128x128
                mock_scale.assert_called_with(mock_snake_image, (128, 128))
                
                # Verify scaled image was blitted to screen
                self.mock_screen.blit.assert_called()

    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_draw_splash_graphics_fallback_when_image_missing(self, mock_exists, mock_load):
        """Test _draw_splash_graphics falls back to custom snake when image is missing."""
        # Mock that the perfect snake image doesn't exist
        mock_exists.return_value = False
        
        with patch.object(self.renderer, "_ensure_images_loaded"), \
             patch.object(self.renderer, "_draw_decorative_fruit_image"), \
             patch.object(self.renderer, "_draw_custom_snake_logo") as mock_custom_snake:
            
            self.renderer._draw_splash_graphics()
            
            # Verify fallback to custom snake was called
            mock_custom_snake.assert_called_once_with(402, 100)  # center_x, snake_y
            
            # Verify image loading was not attempted
            mock_load.assert_not_called()

    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_draw_splash_graphics_fallback_when_image_load_fails(self, mock_exists, mock_load):
        """Test _draw_splash_graphics falls back to custom snake when image loading fails."""
        # Mock that the image exists but loading fails
        mock_exists.return_value = True
        mock_load.side_effect = pygame.error("Failed to load image")
        
        with patch.object(self.renderer, "_ensure_images_loaded"), \
             patch.object(self.renderer, "_draw_decorative_fruit_image"), \
             patch.object(self.renderer, "_draw_custom_snake_logo") as mock_custom_snake:
            
            self.renderer._draw_splash_graphics()
            
            # Verify fallback to custom snake was called
            mock_custom_snake.assert_called_once_with(402, 100)

    def test_draw_splash_graphics_draws_decorative_fruits(self):
        """Test _draw_splash_graphics draws decorative fruits in correct positions."""
        with patch.object(self.renderer, "_ensure_images_loaded"), \
             patch.object(self.renderer, "_draw_decorative_fruit_image") as mock_draw_fruit, \
             patch("snake_game.views.renderer.os.path.exists", return_value=False), \
             patch.object(self.renderer, "_draw_custom_snake_logo"):
            
            self.renderer._draw_splash_graphics()
            
            # Verify decorative fruits are drawn
            assert mock_draw_fruit.call_count == 8  # 8 fruit positions
            
            # Check some specific fruit positions and types
            calls = mock_draw_fruit.call_args_list
            
            # Top corners (WINDOW_WIDTH = 804)
            assert (80, 150, FruitType.APPLE) in [call[0] for call in calls]
            assert (724, 140, FruitType.BANANA) in [call[0] for call in calls]  # 804 - 80 = 724
            
            # Side areas
            assert (60, 240, FruitType.CHERRY) in [call[0] for call in calls]
            assert (744, 250, FruitType.ORANGE) in [call[0] for call in calls]  # 804 - 60 = 744

    @patch("snake_game.views.renderer.pygame.font.Font")
    def test_render_splash_screen_calls_components(self, mock_font):
        """Test render_splash_screen calls all necessary components."""
        mock_font_instance = Mock()
        mock_font.return_value = mock_font_instance
        mock_font_instance.render.return_value = Mock()
        
        with patch.object(self.renderer, "_draw_splash_graphics") as mock_graphics:
            
            self.renderer.render_splash_screen()
            
            # Verify screen was filled with black
            self.mock_screen.fill.assert_called()
            
            # Verify graphics were drawn
            mock_graphics.assert_called_once()
            
            # The font rendering happens in the main method, not in _draw_splash_graphics
            # So we just verify the method was called
            assert True  # Test passes if no exceptions are raised

    def test_get_assets_directory_path(self):
        """Test _get_assets_directory returns correct path."""
        assets_dir = self.renderer._get_assets_directory()
        
        # Should end with the correct path structure
        assert assets_dir.endswith(os.path.join("snake_game", "assets", "images"))
        assert os.path.isabs(assets_dir)  # Should be absolute path

    @patch("snake_game.views.renderer.pygame.image.load")
    @patch("snake_game.views.renderer.os.path.exists")
    def test_perfect_snake_image_scaling_size(self, mock_exists, mock_load):
        """Test that the perfect snake image is scaled to the correct size."""
        mock_exists.return_value = True
        mock_snake_image = Mock()
        mock_snake_image.convert_alpha.return_value = mock_snake_image
        mock_load.return_value = mock_snake_image
        
        with patch("snake_game.views.renderer.pygame.transform.scale") as mock_scale:
            mock_scaled_image = Mock()
            mock_scaled_image.get_rect.return_value = Mock(center=(400, 100))
            mock_scale.return_value = mock_scaled_image
            
            with patch.object(self.renderer, "_ensure_images_loaded"), \
                 patch.object(self.renderer, "_draw_decorative_fruit_image"):
                
                self.renderer._draw_splash_graphics()
                
                # Verify image is scaled to exactly 128x128 pixels
                mock_scale.assert_called_once_with(mock_snake_image, (128, 128))

    def test_snake_positioning_on_splash_screen(self):
        """Test that the snake is positioned correctly on the splash screen."""
        with patch("snake_game.views.renderer.os.path.exists", return_value=False), \
             patch.object(self.renderer, "_ensure_images_loaded"), \
             patch.object(self.renderer, "_draw_decorative_fruit_image"), \
             patch.object(self.renderer, "_draw_custom_snake_logo") as mock_custom_snake:
            
            self.renderer._draw_splash_graphics()
            
            # Verify snake is positioned at center horizontally, y=100
            expected_center_x = 402  # WINDOW_WIDTH // 2 (assuming 804 width)
            expected_y = 100
            mock_custom_snake.assert_called_once_with(expected_center_x, expected_y)


class TestSplashScreenIntegration:
    """Integration tests for splash screen functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        pygame.init()
        self.mock_screen = Mock()
        self.renderer = GameRenderer(self.mock_screen)

    def teardown_method(self):
        """Clean up after tests."""
        pygame.quit()

    def test_splash_screen_with_real_image_file(self):
        """Test splash screen with actual image file if it exists."""
        assets_dir = self.renderer._get_assets_directory()
        snake_path = os.path.join(assets_dir, "perfect_coiled_snake_large.png")
        
        with patch.object(self.renderer, "_draw_decorative_fruit_image"):
            if os.path.exists(snake_path):
                # If the image exists, test that it loads without pygame errors
                with patch("snake_game.views.renderer.pygame.image.load") as mock_load, \
                     patch("snake_game.views.renderer.pygame.transform.scale") as mock_scale:
                    
                    mock_image = Mock()
                    mock_image.convert_alpha.return_value = mock_image
                    mock_load.return_value = mock_image
                    
                    mock_scaled = Mock()
                    mock_scaled.get_rect.return_value = Mock(center=(400, 100))
                    mock_scale.return_value = mock_scaled
                    
                    # This should not raise an exception
                    self.renderer._draw_splash_graphics()
                    
                    # Verify snake image loading was attempted (among other images)
                    snake_calls = [call for call in mock_load.call_args_list 
                                 if snake_path in str(call)]
                    assert len(snake_calls) > 0, "Snake image should have been loaded"
                    
                    # Verify scaling was called
                    assert mock_scale.call_count > 0
            else:
                # If image doesn't exist, should fall back gracefully
                with patch.object(self.renderer, "_draw_custom_snake_logo") as mock_custom:
                    
                    self.renderer._draw_splash_graphics()
                    
                    # Should fall back to custom snake
                    mock_custom.assert_called_once()
