"""Game renderer for the Snake Game."""

import math
import os
from typing import List

import pygame

from snake_game.models import Fruit, FruitType, Snake
from snake_game.utils import GameConstants
from snake_game.utils.path_smoother import PathSmoother
from snake_game.views.snake_renderer import (
    SnakeBodyRenderer,
    SnakeHeadRenderer,
    SnakeScaleRenderer,
)


class GameRenderer:
    """Handles all game rendering and visual effects with refactored architecture."""

    def __init__(self, screen: pygame.Surface):
        """Initialize the game renderer.

        Args:
            screen: Pygame surface to render to
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)

        # Initialize component renderers
        self.snake_body_renderer = SnakeBodyRenderer(screen)
        self.snake_head_renderer = SnakeHeadRenderer(screen)
        self.snake_scale_renderer = SnakeScaleRenderer(screen)

        # Load fruit images (after pygame display is initialized)
        self.fruit_images = {}
        self.use_images = False
        # Delay loading until first render to ensure pygame is fully initialized
        self._images_loaded = False

    def _ensure_images_loaded(self):
        """Ensure fruit images are loaded (called on first render)."""
        if not self._images_loaded:
            self.use_images = self.load_fruit_images()
            self._images_loaded = True

    def load_fruit_images(self):
        """Load high-quality fruit images.

        Returns:
            True if images were loaded successfully, False otherwise
        """
        try:
            assets_dir = self._get_assets_directory()
            fruit_names = ["apple", "pear", "banana", "cherry", "orange"]

            loaded_count = 0
            for fruit_name in fruit_names:
                if self._load_single_fruit_image(assets_dir, fruit_name):
                    loaded_count += 1

            return self._handle_image_loading_result(loaded_count)
        except Exception as e:
            print(f"Error loading fruit images: {e}")
            return False

    def _get_assets_directory(self) -> str:
        """Get the path to the assets directory."""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "images"
        )

    def _load_single_fruit_image(self, assets_dir: str, fruit_name: str) -> bool:
        """Load a single fruit image.

        Args:
            assets_dir: Path to assets directory
            fruit_name: Name of the fruit

        Returns:
            True if loaded successfully, False otherwise
        """
        image_path = os.path.join(assets_dir, f"{fruit_name}.png")
        try:
            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()
                self.fruit_images[fruit_name] = image
                return True
            else:
                print(f"Warning: Could not find {image_path}")
                return False
        except Exception as e:
            print(f"Warning: Could not load {fruit_name} image: {e}")
            return False

    def _handle_image_loading_result(self, loaded_count: int) -> bool:
        """Handle the result of image loading.

        Args:
            loaded_count: Number of images successfully loaded

        Returns:
            True if any images were loaded, False otherwise
        """
        return loaded_count > 0

    def render_splash_screen(self):
        """Render the splash screen."""
        self.screen.fill(GameConstants.BLACK)

        # Draw splash graphics
        self._draw_splash_graphics()

        # Title with shadow effect
        title_shadow = self.large_font.render(
            "SNAKE GAME", True, GameConstants.DARK_GREEN
        )
        title_text = self.large_font.render("SNAKE GAME", True, GameConstants.GREEN)
        title_rect = title_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 200))
        shadow_rect = title_shadow.get_rect(
            center=(GameConstants.WINDOW_WIDTH // 2 + 3, 203)
        )
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title_text, title_rect)

        # Instructions
        instructions = [
            "Use arrow keys to control the snake",
            "Eat different fruits to grow and score points",
            "Avoid hitting walls and yourself",
            "Each fruit gives 4 points and increases speed",
            "",
            "Press any key to start!",
            "Press H to view high scores",
            "Press Q to quit",
        ]

        y_offset = 280
        for instruction in instructions:
            if instruction:  # Skip empty lines
                color = (
                    GameConstants.YELLOW
                    if "Press" in instruction
                    else GameConstants.WHITE
                )
                text = self.small_font.render(instruction, True, color)
                text_rect = text.get_rect(
                    center=(GameConstants.WINDOW_WIDTH // 2, y_offset)
                )
                self.screen.blit(text, text_rect)
            y_offset += 25

    def render_game_screen(self, snake: Snake, fruit: Fruit, score: int, speed: int):
        """Render the main game screen.

        Args:
            snake: Snake object to render
            fruit: Fruit object to render
            score: Current score
            speed: Current game speed
        """
        self.screen.fill(GameConstants.BLACK)

        # Draw UI and border
        self._draw_ui(score, snake.length, speed)
        self._draw_border()

        # Draw snake
        self._draw_snake(snake)

        # Draw fruit
        self._draw_fruit(fruit)

    def render_game_over_screen(self, final_score: int, is_high_score: bool):
        """Render the game over screen.

        Args:
            final_score: The final score achieved
            is_high_score: Whether this is a new high score
        """
        self.screen.fill(GameConstants.BLACK)

        # Game Over title with pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        red_color = (int(255 * pulse), 0, 0)

        game_over_text = self.large_font.render("GAME OVER!", True, red_color)
        game_over_rect = game_over_text.get_rect(
            center=(GameConstants.WINDOW_WIDTH // 2, 150)
        )
        self.screen.blit(game_over_text, game_over_rect)

        # Final score
        score_text = self.font.render(
            f"Final Score: {final_score:,}", True, GameConstants.WHITE
        )
        score_rect = score_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)

        # Check if it's a high score
        if is_high_score and final_score > 0:
            high_score_text = self.font.render(
                "NEW HIGH SCORE!", True, GameConstants.YELLOW
            )
            high_score_rect = high_score_text.get_rect(
                center=(GameConstants.WINDOW_WIDTH // 2, 260)
            )
            self.screen.blit(high_score_text, high_score_rect)

        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press H to view high scores",
            "Press Q to quit",
        ]

        y_offset = 320
        for instruction in instructions:
            text = self.small_font.render(instruction, True, GameConstants.WHITE)
            text_rect = text.get_rect(
                center=(GameConstants.WINDOW_WIDTH // 2, y_offset)
            )
            self.screen.blit(text, text_rect)
            y_offset += 30

    def render_high_scores_screen(self, high_scores: List[int]):
        """Render the high scores screen.

        Args:
            high_scores: List of high scores to display
        """
        self.screen.fill(GameConstants.BLACK)

        # Title
        title_text = self.large_font.render("HIGH SCORES", True, GameConstants.YELLOW)
        title_rect = title_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)

        # High scores with ranking colors
        colors = [
            GameConstants.YELLOW,
            GameConstants.LIGHT_GRAY,
            GameConstants.BROWN,
            GameConstants.WHITE,
            GameConstants.WHITE,
        ]
        y_offset = 180
        for i, score in enumerate(high_scores):
            color = colors[i] if i < len(colors) else GameConstants.WHITE
            score_text = self.font.render(f"{i + 1}. {score:,}", True, color)
            score_rect = score_text.get_rect(
                center=(GameConstants.WINDOW_WIDTH // 2, y_offset)
            )
            self.screen.blit(score_text, score_rect)
            y_offset += 40

        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press ESC to return to splash screen",
            "Press Q to quit",
        ]

        y_offset = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, GameConstants.WHITE)
            text_rect = text.get_rect(
                center=(GameConstants.WINDOW_WIDTH // 2, y_offset)
            )
            self.screen.blit(text, text_rect)
            y_offset += 25

    def render_confirm_reset_screen(self):
        """Render the confirmation screen for resetting high scores."""
        self.screen.fill(GameConstants.BLACK)

        # Warning title
        warning_text = self.large_font.render(
            "RESET HIGH SCORES?", True, GameConstants.RED
        )
        warning_rect = warning_text.get_rect(
            center=(GameConstants.WINDOW_WIDTH // 2, 200)
        )
        self.screen.blit(warning_text, warning_rect)

        # Confirmation message
        confirm_text = self.font.render(
            "This will reset all high scores to 0", True, GameConstants.WHITE
        )
        confirm_rect = confirm_text.get_rect(
            center=(GameConstants.WINDOW_WIDTH // 2, 260)
        )
        self.screen.blit(confirm_text, confirm_rect)

        # Instructions
        instructions = ["Press Y to confirm reset", "Press N or ESC to cancel"]

        y_offset = 320
        for instruction in instructions:
            color = (
                GameConstants.RED
                if "Y to confirm" in instruction
                else GameConstants.WHITE
            )
            text = self.font.render(instruction, True, color)
            text_rect = text.get_rect(
                center=(GameConstants.WINDOW_WIDTH // 2, y_offset)
            )
            self.screen.blit(text, text_rect)
            y_offset += 40

    def _draw_splash_graphics(self):
        """Draw graphics for the splash screen using high-quality Twemoji images."""
        # Ensure images are loaded
        self._ensure_images_loaded()

        # Draw a single large snake logo as the main logo
        center_x = GameConstants.WINDOW_WIDTH // 2
        snake_y = 100
        
        # Use the perfect coiled snake image
        snake_path = os.path.join(self._get_assets_directory(), "perfect_coiled_snake_large.png")
        
        if os.path.exists(snake_path):
            try:
                snake_image = pygame.image.load(snake_path).convert_alpha()
                # Scale up the snake image to make it more prominent (128x128, about 33% larger)
                scaled_snake = pygame.transform.scale(snake_image, (128, 128))
                snake_rect = scaled_snake.get_rect()
                snake_rect.center = (center_x, snake_y)
                self.screen.blit(scaled_snake, snake_rect)
            except Exception as e:
                print(f"Warning: Could not load perfect coiled snake: {e}")
                # Fallback to custom drawn snake
                self._draw_custom_snake_logo(center_x, snake_y)
        else:
            # Fallback to custom drawn snake if image not found
            self._draw_custom_snake_logo(center_x, snake_y)

        # Draw high-quality Twemoji fruits around the screen (avoiding text areas)
        # Text areas: Title at y=200, Instructions from y=280 to y=480
        # Safe areas: Top corners, sides, and bottom
        fruits = [
            # Top corners (above title)
            (80, 150, FruitType.APPLE),
            (GameConstants.WINDOW_WIDTH - 80, 140, FruitType.BANANA),
            # Side areas (between title and instructions)
            (60, 240, FruitType.CHERRY),
            (GameConstants.WINDOW_WIDTH - 60, 250, FruitType.ORANGE),
            # Bottom area (below instructions)
            (center_x - 60, 520, FruitType.PEAR),
            (center_x + 60, 510, FruitType.APPLE),
            # Additional decorative fruits in safe areas
            (120, 480, FruitType.BANANA),
            (GameConstants.WINDOW_WIDTH - 120, 490, FruitType.CHERRY),
        ]

        for x, y, fruit_type in fruits:
            self._draw_decorative_fruit_image(x, y, fruit_type)

    def _draw_custom_snake_logo(self, center_x: int, center_y: int):
        """Draw a custom snake logo as fallback when emoji is not available.
        
        Args:
            center_x: Center X position for the snake
            center_y: Center Y position for the snake
        """
        # Draw a decorative snake
        snake_points = []
        for i in range(8):
            x = center_x - 100 + i * 25
            y = center_y + int(20 * math.sin(i * 0.5))
            snake_points.append((x, y))

        # Draw snake body
        for i, (x, y) in enumerate(snake_points):
            color = (
                GameConstants.GREEN
                if i == len(snake_points) - 1
                else GameConstants.DARK_GREEN
            )
            pygame.draw.circle(self.screen, color, (x, y), 12)
            if i == len(snake_points) - 1:  # Head
                # Eyes
                pygame.draw.circle(self.screen, GameConstants.WHITE, (x + 4, y - 3), 3)
                pygame.draw.circle(self.screen, GameConstants.WHITE, (x + 4, y + 3), 3)
                pygame.draw.circle(self.screen, GameConstants.BLACK, (x + 4, y - 3), 2)
                pygame.draw.circle(self.screen, GameConstants.BLACK, (x + 4, y + 3), 2)

    def _draw_decorative_fruit_image(self, x: int, y: int, fruit_type: FruitType):
        """Draw a decorative fruit using high-quality Twemoji images when available.

        Args:
            x: X position
            y: Y position
            fruit_type: Type of fruit to draw
        """
        name, primary_color, secondary_color = fruit_type.value

        if self.use_images and name in self.fruit_images:
            # Use high-quality Twemoji image, scaled up for splash screen
            image = self.fruit_images[name]
            # Scale up the image for better visibility on splash screen
            scaled_image = pygame.transform.scale(
                image, (32, 32)
            )  # 1.6x larger than game size

            # Center the image at the given position
            image_rect = scaled_image.get_rect()
            image_rect.center = (x, y)

            self.screen.blit(scaled_image, image_rect)
        else:
            # Fallback to enhanced custom graphics
            self._draw_decorative_fruit_custom(x, y, fruit_type)

    def _draw_decorative_fruit_custom(self, x: int, y: int, fruit_type: FruitType):
        """Draw a decorative fruit with enhanced custom graphics as fallback.

        Args:
            x: X position
            y: Y position
            fruit_type: Type of fruit to draw
        """
        name, primary_color, secondary_color = fruit_type.value

        fruit_drawers = {
            "apple": self._draw_decorative_apple,
            "banana": self._draw_decorative_banana,
            "cherry": self._draw_decorative_cherry,
            "orange": self._draw_decorative_orange,
            "pear": self._draw_decorative_pear,
        }

        drawer = fruit_drawers.get(name)
        if drawer:
            drawer(x, y)

    def _draw_decorative_apple(self, x: int, y: int):
        """Draw a decorative apple."""
        pygame.draw.circle(self.screen, (220, 20, 20), (x, y + 2), 14)
        pygame.draw.circle(self.screen, (255, 50, 50), (x - 3, y - 1), 10)
        pygame.draw.rect(self.screen, (101, 67, 33), (x - 1, y - 10, 2, 6))
        pygame.draw.ellipse(self.screen, (34, 139, 34), (x + 1, y - 10, 8, 4))
        pygame.draw.circle(self.screen, (255, 200, 200), (x - 4, y - 3), 3)

    def _draw_decorative_banana(self, x: int, y: int):
        """Draw a decorative banana."""
        points = [
            (x - 10, y + 4),
            (x - 8, y - 10),
            (x + 4, y - 8),
            (x + 12, y + 8),
            (x + 6, y + 10),
            (x - 8, y + 8),
        ]
        pygame.draw.polygon(self.screen, (255, 255, 0), points)
        pygame.draw.circle(self.screen, (101, 67, 33), (x - 8, y - 10), 3)
        pygame.draw.line(self.screen, (200, 200, 0), (x - 6, y - 6), (x + 6, y + 4), 2)

    def _draw_decorative_cherry(self, x: int, y: int):
        """Draw decorative cherries."""
        pygame.draw.circle(self.screen, (139, 0, 0), (x - 5, y + 3), 9)
        pygame.draw.circle(self.screen, (220, 20, 60), (x - 5, y + 3), 7)
        pygame.draw.circle(self.screen, (139, 0, 0), (x + 5, y + 4), 9)
        pygame.draw.circle(self.screen, (220, 20, 60), (x + 5, y + 4), 7)
        pygame.draw.line(self.screen, (34, 139, 34), (x - 5, y - 6), (x - 2, y - 12), 3)
        pygame.draw.line(self.screen, (34, 139, 34), (x + 5, y - 5), (x + 2, y - 12), 3)
        pygame.draw.circle(self.screen, (255, 100, 100), (x - 7, y + 1), 3)
        pygame.draw.circle(self.screen, (255, 100, 100), (x + 3, y + 2), 3)

    def _draw_decorative_orange(self, x: int, y: int):
        """Draw a decorative orange."""
        pygame.draw.circle(self.screen, (255, 140, 0), (x, y), 14)
        pygame.draw.circle(self.screen, (255, 165, 0), (x - 2, y - 2), 10)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue
                dot_x = x + i * 4
                dot_y = y + j * 4
                if (dot_x - x) ** 2 + (dot_y - y) ** 2 <= 100:
                    pygame.draw.circle(self.screen, (200, 100, 0), (dot_x, dot_y), 1)
        pygame.draw.circle(self.screen, (34, 139, 34), (x, y - 12), 3)

    def _draw_decorative_pear(self, x: int, y: int):
        """Draw a decorative pear."""
        pygame.draw.circle(self.screen, (255, 255, 100), (x, y + 5), 10)
        pygame.draw.circle(self.screen, (200, 255, 100), (x, y - 2), 7)
        pygame.draw.rect(self.screen, (101, 67, 33), (x - 1, y - 12, 2, 6))
        pygame.draw.circle(self.screen, (255, 255, 200), (x - 3, y), 3)

    def _draw_ui(self, score: int, length: int, speed: int):
        """Draw the UI area with score and length.

        Args:
            score: Current score
            length: Snake length
            speed: Current speed
        """
        # UI background
        ui_rect = pygame.Rect(0, 0, GameConstants.WINDOW_WIDTH, GameConstants.UI_HEIGHT)
        pygame.draw.rect(self.screen, GameConstants.GRAY, ui_rect)
        pygame.draw.rect(self.screen, GameConstants.WHITE, ui_rect, 2)

        # Score
        score_text = self.font.render(f"Score: {score:,}", True, GameConstants.WHITE)
        self.screen.blit(score_text, (10, 15))

        # Length
        length_text = self.font.render(f"Length: {length}", True, GameConstants.WHITE)
        self.screen.blit(length_text, (200, 15))

        # Speed indicator
        speed_percent = max(
            0,
            100
            - int(
                (speed - GameConstants.MIN_SPEED)
                / (GameConstants.INITIAL_SPEED - GameConstants.MIN_SPEED)
                * 100
            ),
        )
        speed_text = self.small_font.render(
            f"Speed: {speed_percent}%", True, GameConstants.WHITE
        )
        self.screen.blit(speed_text, (400, 20))

        # Quit instruction
        quit_text = self.small_font.render(
            "Press Q to quit", True, GameConstants.LIGHT_GRAY
        )
        self.screen.blit(quit_text, (GameConstants.WINDOW_WIDTH - 120, 20))

    def _draw_border(self):
        """Draw the game border."""
        # Outer border
        border_rect = pygame.Rect(
            0,
            GameConstants.UI_HEIGHT,
            GameConstants.WINDOW_WIDTH,
            GameConstants.PLAY_AREA_HEIGHT + GameConstants.BORDER_WIDTH * 2,
        )
        pygame.draw.rect(
            self.screen, GameConstants.BROWN, border_rect, GameConstants.BORDER_WIDTH
        )

        # Inner playing area background
        play_rect = pygame.Rect(
            GameConstants.PLAY_AREA_X,
            GameConstants.PLAY_AREA_Y,
            GameConstants.PLAY_AREA_WIDTH,
            GameConstants.PLAY_AREA_HEIGHT,
        )
        pygame.draw.rect(self.screen, GameConstants.BLACK, play_rect)

    def _draw_snake(self, snake: Snake):
        """Draw the snake using component renderers for clean separation of concerns.

        Args:
            snake: Snake object to draw
        """
        if len(snake.segments) < 2:
            # If only head, draw it normally
            if snake.segments:
                head_x, head_y = snake.segments[0]
                self.snake_head_renderer.draw_head(head_x, head_y, snake.direction)
            return

        # Convert grid positions to screen coordinates
        screen_points = PathSmoother.convert_segments_to_screen_points(snake.segments)

        # Create smooth path points for the snake body
        smooth_points = PathSmoother.create_smooth_path(screen_points)

        # Draw the continuous snake body using component renderer
        self.snake_body_renderer.draw_body(smooth_points, snake.segments)

        # Add scale patterns using component renderer
        self.snake_scale_renderer.draw_scales(smooth_points)

        # Draw head last (on top) using component renderer
        head_x, head_y = snake.segments[0]
        self.snake_head_renderer.draw_head(head_x, head_y, snake.direction)

    def _draw_fruit(self, fruit: Fruit):
        """Draw a fruit using high-quality emoji images when available.

        Args:
            fruit: Fruit object to draw
        """
        # Ensure images are loaded
        self._ensure_images_loaded()

        x, y = fruit.position
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE

        fruit_name = fruit.name

        if self.use_images and fruit_name in self.fruit_images:
            # Use high-quality emoji image
            image = self.fruit_images[fruit_name]
            # Center the image in the cell
            image_rect = image.get_rect()
            image_rect.center = (
                screen_x + GameConstants.CELL_SIZE // 2,
                screen_y + GameConstants.CELL_SIZE // 2,
            )
            self.screen.blit(image, image_rect)
        else:
            # Fallback to custom graphics
            self._draw_fruit_custom(screen_x, screen_y, fruit)

    def _draw_fruit_custom(self, screen_x: int, screen_y: int, fruit: Fruit):
        """Draw fruit using custom graphics as fallback.

        Args:
            screen_x: Screen X position
            screen_y: Screen Y position
            fruit: Fruit object
        """
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2

        fruit_drawers = {
            "apple": self._draw_custom_apple,
            "pear": self._draw_custom_pear,
            "banana": self._draw_custom_banana,
            "cherry": self._draw_custom_cherry,
            "orange": self._draw_custom_orange,
        }

        drawer = fruit_drawers.get(fruit.name)
        if drawer:
            drawer(center_x, center_y, screen_x, screen_y)

    def _draw_custom_apple(
        self, center_x: int, center_y: int, screen_x: int, screen_y: int
    ):
        """Draw a custom apple."""
        pygame.draw.circle(self.screen, (220, 20, 20), (center_x, center_y + 1), 9)
        pygame.draw.circle(self.screen, (255, 50, 50), (center_x - 2, center_y - 1), 7)
        pygame.draw.rect(self.screen, (101, 67, 33), (center_x - 1, screen_y + 3, 2, 5))
        pygame.draw.ellipse(
            self.screen, (34, 139, 34), (center_x + 1, screen_y + 3, 6, 3)
        )
        pygame.draw.circle(
            self.screen, (255, 200, 200), (center_x - 3, center_y - 2), 2
        )

    def _draw_custom_pear(
        self, center_x: int, center_y: int, screen_x: int, screen_y: int
    ):
        """Draw a custom pear."""
        pygame.draw.circle(self.screen, (255, 255, 100), (center_x, center_y + 3), 7)
        pygame.draw.circle(self.screen, (200, 255, 100), (center_x, center_y - 1), 5)
        pygame.draw.rect(self.screen, (101, 67, 33), (center_x - 1, screen_y + 3, 2, 4))
        pygame.draw.circle(self.screen, (255, 255, 200), (center_x - 2, center_y), 2)

    def _draw_custom_banana(
        self, center_x: int, center_y: int, screen_x: int, screen_y: int
    ):
        """Draw a custom banana."""
        points = [
            (center_x - 7, center_y + 3),
            (center_x - 5, center_y - 7),
            (center_x + 1, center_y - 6),
            (center_x + 7, center_y + 5),
            (center_x + 4, center_y + 7),
            (center_x - 4, center_y + 5),
        ]
        pygame.draw.polygon(self.screen, (255, 255, 0), points)
        pygame.draw.circle(self.screen, (101, 67, 33), (center_x - 5, center_y - 7), 2)
        pygame.draw.line(
            self.screen,
            (200, 200, 0),
            (center_x - 4, center_y - 4),
            (center_x + 3, center_y + 3),
            1,
        )
        pygame.draw.line(
            self.screen,
            (200, 200, 0),
            (center_x - 2, center_y - 5),
            (center_x + 5, center_y + 2),
            1,
        )

    def _draw_custom_cherry(
        self, center_x: int, center_y: int, screen_x: int, screen_y: int
    ):
        """Draw custom cherries."""
        pygame.draw.circle(self.screen, (139, 0, 0), (center_x - 3, center_y + 2), 6)
        pygame.draw.circle(self.screen, (220, 20, 60), (center_x - 3, center_y + 2), 5)
        pygame.draw.circle(self.screen, (139, 0, 0), (center_x + 3, center_y + 3), 6)
        pygame.draw.circle(self.screen, (220, 20, 60), (center_x + 3, center_y + 3), 5)
        pygame.draw.line(
            self.screen,
            (34, 139, 34),
            (center_x - 3, center_y - 4),
            (center_x - 1, center_y - 7),
            2,
        )
        pygame.draw.line(
            self.screen,
            (34, 139, 34),
            (center_x + 3, center_y - 3),
            (center_x + 1, center_y - 7),
            2,
        )
        pygame.draw.circle(
            self.screen, (255, 100, 100), (center_x - 4, center_y + 1), 2
        )
        pygame.draw.circle(
            self.screen, (255, 100, 100), (center_x + 2, center_y + 2), 2
        )

    def _draw_custom_orange(
        self, center_x: int, center_y: int, screen_x: int, screen_y: int
    ):
        """Draw a custom orange."""
        pygame.draw.circle(self.screen, (255, 140, 0), (center_x, center_y), 9)
        pygame.draw.circle(self.screen, (255, 165, 0), (center_x - 1, center_y - 1), 7)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                dot_x = center_x + i * 3
                dot_y = center_y + j * 3
                if (dot_x - center_x) ** 2 + (dot_y - center_y) ** 2 <= 49:
                    pygame.draw.circle(self.screen, (200, 100, 0), (dot_x, dot_y), 1)
        pygame.draw.circle(self.screen, (34, 139, 34), (center_x, center_y - 8), 2)
