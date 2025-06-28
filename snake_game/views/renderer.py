"""Game renderer for the Snake Game."""

import pygame
import math
from typing import List, Tuple
from ..models import Snake, Fruit, GameState, FruitType, Direction
from ..utils import GameConstants


class GameRenderer:
    """Handles all game rendering and visual effects."""
    
    def __init__(self, screen: pygame.Surface):
        """Initialize the game renderer.
        
        Args:
            screen: Pygame surface to render to
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
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
        import os
        
        try:
            # Path to fruit images
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images')
            
            fruit_names = ['apple', 'pear', 'banana', 'cherry', 'orange']
            
            for fruit_name in fruit_names:
                image_path = os.path.join(assets_dir, f'{fruit_name}.png')
                try:
                    if os.path.exists(image_path):
                        # Load and convert image for optimal blitting
                        image = pygame.image.load(image_path).convert_alpha()
                        self.fruit_images[fruit_name] = image
                    else:
                        print(f"Warning: Could not find {image_path}")
                except Exception as e:
                    print(f"Warning: Could not load {fruit_name} image: {e}")
            
            if self.fruit_images:
                print(f"✓ Loaded {len(self.fruit_images)} high-quality Twemoji fruit images")
                return True
            else:
                print("⚠️  No fruit images loaded, falling back to custom graphics")
                return False
        except Exception as e:
            print(f"Error loading fruit images: {e}")
            return False
    
    def render_splash_screen(self):
        """Render the splash screen."""
        self.screen.fill(GameConstants.BLACK)
        
        # Draw splash graphics
        self._draw_splash_graphics()
        
        # Title with shadow effect
        title_shadow = self.large_font.render("SNAKE GAME", True, GameConstants.DARK_GREEN)
        title_text = self.large_font.render("SNAKE GAME", True, GameConstants.GREEN)
        title_rect = title_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 200))
        shadow_rect = title_shadow.get_rect(center=(GameConstants.WINDOW_WIDTH // 2 + 3, 203))
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
            "Press Q to quit"
        ]
        
        y_offset = 280
        for instruction in instructions:
            if instruction:  # Skip empty lines
                color = GameConstants.YELLOW if "Press" in instruction else GameConstants.WHITE
                text = self.small_font.render(instruction, True, color)
                text_rect = text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, y_offset))
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
        game_over_rect = game_over_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {final_score:,}", True, GameConstants.WHITE)
        score_rect = score_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Check if it's a high score
        if is_high_score and final_score > 0:
            high_score_text = self.font.render("NEW HIGH SCORE!", True, GameConstants.YELLOW)
            high_score_rect = high_score_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 260))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press H to view high scores",
            "Press Q to quit"
        ]
        
        y_offset = 320
        for instruction in instructions:
            text = self.small_font.render(instruction, True, GameConstants.WHITE)
            text_rect = text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, y_offset))
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
        colors = [GameConstants.YELLOW, GameConstants.LIGHT_GRAY, GameConstants.BROWN, 
                 GameConstants.WHITE, GameConstants.WHITE]
        y_offset = 180
        for i, score in enumerate(high_scores):
            color = colors[i] if i < len(colors) else GameConstants.WHITE
            score_text = self.font.render(f"{i + 1}. {score:,}", True, color)
            score_rect = score_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(score_text, score_rect)
            y_offset += 40
        
        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press ESC to return to splash screen",
            "Press Q to quit"
        ]
        
        y_offset = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, GameConstants.WHITE)
            text_rect = text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def render_confirm_reset_screen(self):
        """Render the confirmation screen for resetting high scores."""
        self.screen.fill(GameConstants.BLACK)
        
        # Warning title
        warning_text = self.large_font.render("RESET HIGH SCORES?", True, GameConstants.RED)
        warning_rect = warning_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 200))
        self.screen.blit(warning_text, warning_rect)
        
        # Confirmation message
        confirm_text = self.font.render("This will reset all high scores to 0", True, GameConstants.WHITE)
        confirm_rect = confirm_text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, 260))
        self.screen.blit(confirm_text, confirm_rect)
        
        # Instructions
        instructions = [
            "Press Y to confirm reset",
            "Press N or ESC to cancel"
        ]
        
        y_offset = 320
        for instruction in instructions:
            color = GameConstants.RED if "Y to confirm" in instruction else GameConstants.WHITE
            text = self.font.render(instruction, True, color)
            text_rect = text.get_rect(center=(GameConstants.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
    
    def _draw_splash_graphics(self):
        """Draw graphics for the splash screen using high-quality Twemoji images."""
        # Ensure images are loaded
        self._ensure_images_loaded()
        
        # Draw a decorative snake
        snake_points = []
        center_x = GameConstants.WINDOW_WIDTH // 2
        for i in range(8):
            x = center_x - 100 + i * 25
            y = 100 + int(20 * math.sin(i * 0.5))
            snake_points.append((x, y))
        
        # Draw snake body
        for i, (x, y) in enumerate(snake_points):
            color = GameConstants.GREEN if i == len(snake_points) - 1 else GameConstants.DARK_GREEN
            pygame.draw.circle(self.screen, color, (x, y), 12)
            if i == len(snake_points) - 1:  # Head
                # Eyes
                pygame.draw.circle(self.screen, GameConstants.WHITE, (x + 4, y - 3), 3)
                pygame.draw.circle(self.screen, GameConstants.WHITE, (x + 4, y + 3), 3)
                pygame.draw.circle(self.screen, GameConstants.BLACK, (x + 4, y - 3), 2)
                pygame.draw.circle(self.screen, GameConstants.BLACK, (x + 4, y + 3), 2)
        
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
            (GameConstants.WINDOW_WIDTH - 120, 490, FruitType.CHERRY)
        ]
        
        for x, y, fruit_type in fruits:
            self._draw_decorative_fruit_image(x, y, fruit_type)
    
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
            scaled_image = pygame.transform.scale(image, (32, 32))  # 1.6x larger than game size
            
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
        
        if name == "apple":
            # Enhanced decorative apple
            pygame.draw.circle(self.screen, (220, 20, 20), (x, y + 2), 14)
            pygame.draw.circle(self.screen, (255, 50, 50), (x - 3, y - 1), 10)
            pygame.draw.rect(self.screen, (101, 67, 33), (x - 1, y - 10, 2, 6))
            pygame.draw.ellipse(self.screen, (34, 139, 34), (x + 1, y - 10, 8, 4))
            pygame.draw.circle(self.screen, (255, 200, 200), (x - 4, y - 3), 3)
        elif name == "banana":
            # Enhanced decorative banana
            points = [
                (x - 10, y + 4), (x - 8, y - 10), (x + 4, y - 8),
                (x + 12, y + 8), (x + 6, y + 10), (x - 8, y + 8)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 0), points)
            pygame.draw.circle(self.screen, (101, 67, 33), (x - 8, y - 10), 3)
            pygame.draw.line(self.screen, (200, 200, 0), (x - 6, y - 6), (x + 6, y + 4), 2)
        elif name == "cherry":
            # Enhanced decorative cherries
            pygame.draw.circle(self.screen, (139, 0, 0), (x - 5, y + 3), 9)
            pygame.draw.circle(self.screen, (220, 20, 60), (x - 5, y + 3), 7)
            pygame.draw.circle(self.screen, (139, 0, 0), (x + 5, y + 4), 9)
            pygame.draw.circle(self.screen, (220, 20, 60), (x + 5, y + 4), 7)
            pygame.draw.line(self.screen, (34, 139, 34), (x - 5, y - 6), (x - 2, y - 12), 3)
            pygame.draw.line(self.screen, (34, 139, 34), (x + 5, y - 5), (x + 2, y - 12), 3)
            pygame.draw.circle(self.screen, (255, 100, 100), (x - 7, y + 1), 3)
            pygame.draw.circle(self.screen, (255, 100, 100), (x + 3, y + 2), 3)
        elif name == "orange":
            # Enhanced decorative orange
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
        elif name == "pear":
            # Enhanced decorative pear
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
        speed_percent = max(0, 100 - int((speed - GameConstants.MIN_SPEED) / 
                                       (GameConstants.INITIAL_SPEED - GameConstants.MIN_SPEED) * 100))
        speed_text = self.small_font.render(f"Speed: {speed_percent}%", True, GameConstants.WHITE)
        self.screen.blit(speed_text, (400, 20))
        
        # Quit instruction
        quit_text = self.small_font.render("Press Q to quit", True, GameConstants.LIGHT_GRAY)
        self.screen.blit(quit_text, (GameConstants.WINDOW_WIDTH - 120, 20))
    
    def _draw_border(self):
        """Draw the game border."""
        # Outer border
        border_rect = pygame.Rect(0, GameConstants.UI_HEIGHT, GameConstants.WINDOW_WIDTH, 
                                GameConstants.PLAY_AREA_HEIGHT + GameConstants.BORDER_WIDTH * 2)
        pygame.draw.rect(self.screen, GameConstants.BROWN, border_rect, GameConstants.BORDER_WIDTH)
        
        # Inner playing area background
        play_rect = pygame.Rect(GameConstants.PLAY_AREA_X, GameConstants.PLAY_AREA_Y, 
                              GameConstants.PLAY_AREA_WIDTH, GameConstants.PLAY_AREA_HEIGHT)
        pygame.draw.rect(self.screen, GameConstants.BLACK, play_rect)
    
    def _draw_snake(self, snake: Snake):
        """Draw the snake as a single, continuous, smooth shape.
        
        Args:
            snake: Snake object to draw
        """
        if len(snake.segments) < 2:
            # If only head, draw it normally
            if snake.segments:
                head_x, head_y = snake.segments[0]
                self._draw_snake_head(head_x, head_y, snake.direction)
            return
        
        # Draw the continuous snake body
        self._draw_continuous_snake_body(snake.segments)
        
        # Draw head last (on top)
        head_x, head_y = snake.segments[0]
        self._draw_snake_head(head_x, head_y, snake.direction)
    
    def _draw_continuous_snake_body(self, segments: list):
        """Draw the snake as a single continuous, smooth shape.
        
        Args:
            segments: List of snake segment positions
        """
        if len(segments) < 2:
            return
        
        # Convert grid positions to screen coordinates
        screen_points = []
        for x, y in segments:
            screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE + GameConstants.CELL_SIZE // 2
            screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE + GameConstants.CELL_SIZE // 2
            screen_points.append((screen_x, screen_y))
        
        # Create smooth path points for the snake body
        smooth_points = self._create_smooth_snake_path(screen_points)
        
        # Draw the continuous snake body with varying thickness
        self._draw_smooth_snake_body(smooth_points, segments)
    
    def _create_smooth_snake_path(self, points: list):
        """Create a smooth path through the snake segments.
        
        Args:
            points: List of screen coordinate points
            
        Returns:
            List of smoothed points for drawing
        """
        if len(points) < 3:
            return points
        
        smooth_points = [points[0]]  # Start with head
        
        # Create smooth curves between segments
        for i in range(1, len(points) - 1):
            prev_point = points[i - 1]
            curr_point = points[i]
            next_point = points[i + 1]
            
            # Calculate smooth curve points around corners
            curve_points = self._calculate_corner_curve(prev_point, curr_point, next_point)
            smooth_points.extend(curve_points)
        
        smooth_points.append(points[-1])  # End with tail
        return smooth_points
    
    def _calculate_corner_curve(self, prev_point, curr_point, next_point):
        """Calculate smooth curve points for a corner.
        
        Args:
            prev_point: Previous segment center
            curr_point: Current segment center  
            next_point: Next segment center
            
        Returns:
            List of points forming a smooth curve
        """
        curve_points = []
        
        # Vector from previous to current
        dx1 = curr_point[0] - prev_point[0]
        dy1 = curr_point[1] - prev_point[1]
        
        # Vector from current to next
        dx2 = next_point[0] - curr_point[0]
        dy2 = next_point[1] - curr_point[1]
        
        # If it's a straight line, just add the current point
        if (dx1 == dx2 and dy1 == dy2) or (dx1 == 0 and dy1 == 0) or (dx2 == 0 and dy2 == 0):
            curve_points.append(curr_point)
            return curve_points
        
        # Create smooth corner with multiple points
        corner_radius = GameConstants.CELL_SIZE // 3
        
        # Calculate curve points
        for t in [0.3, 0.5, 0.7]:  # Smooth interpolation
            # Bezier-like curve calculation
            x = int(curr_point[0] + (dx1 * (1-t) + dx2 * t) * 0.3)
            y = int(curr_point[1] + (dy1 * (1-t) + dy2 * t) * 0.3)
            curve_points.append((x, y))
        
        return curve_points
    
    def _draw_smooth_snake_body(self, points: list, segments: list):
        """Draw the snake body as a smooth, continuous shape.
        
        Args:
            points: Smoothed path points
            segments: Original segment positions for thickness calculation
        """
        if len(points) < 2:
            return
        
        # Draw the snake body with varying thickness and colors
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            
            # Calculate thickness based on position (thicker at head, thinner at tail)
            progress = i / max(1, len(points) - 1)
            base_thickness = 10
            thickness = int(base_thickness * (1.0 - progress * 0.4))  # Taper toward tail
            
            # Calculate colors with gradient
            color_progress = progress
            base_green = int(34 + (50 - 34) * (1 - color_progress))
            mid_green = int(139 + (205 - 139) * (1 - color_progress))
            light_green = int(34 + (60 - 34) * (1 - color_progress))
            
            # Draw multiple layers for 3D effect
            colors_and_thickness = [
                ((base_green, mid_green, base_green), thickness),
                ((50, 205, 50), thickness - 2),
                ((70, 230, 70), thickness - 4),
            ]
            
            for color, thick in colors_and_thickness:
                if thick > 0:
                    self._draw_thick_line(start_point, end_point, color, thick)
        
        # Add scale pattern along the body
        self._draw_snake_scales(points)
    
    def _draw_thick_line(self, start_point, end_point, color, thickness):
        """Draw a thick line between two points with rounded ends.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            color: Line color
            thickness: Line thickness
        """
        # Draw the main line
        if thickness > 1:
            pygame.draw.line(self.screen, color, start_point, end_point, thickness)
            
            # Draw rounded end caps
            radius = thickness // 2
            pygame.draw.circle(self.screen, color, start_point, radius)
            pygame.draw.circle(self.screen, color, end_point, radius)
    
    def _draw_snake_scales(self, points: list):
        """Draw scale patterns along the snake body.
        
        Args:
            points: Path points along the snake body
        """
        scale_spacing = 15  # Distance between scales
        
        for i in range(0, len(points) - 1, scale_spacing):
            if i + 1 < len(points):
                point = points[i]
                
                # Draw small diamond scale
                scale_size = 3
                scale_points = [
                    (point[0] - scale_size, point[1]),
                    (point[0], point[1] - scale_size),
                    (point[0] + scale_size, point[1]),
                    (point[0], point[1] + scale_size)
                ]
                pygame.draw.polygon(self.screen, (40, 160, 40), scale_points)
    
    def _draw_snake_head(self, x: int, y: int, direction: Direction):
        """Draw a realistic snake head with proper shape and flickering tongue.
        
        Args:
            x: Grid x position
            y: Grid y position
            direction: Snake's current direction
        """
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2
        
        # Head shape - more elongated and realistic
        head_width = 12
        head_height = 16
        
        # Adjust head shape based on direction
        if direction in [Direction.LEFT, Direction.RIGHT]:
            head_width, head_height = head_height, head_width
        
        # Draw head with gradient layers for 3D effect
        head_colors = [
            (34, 139, 34),   # Dark green (outer)
            (50, 205, 50),   # Medium green (middle)
            (70, 230, 70),   # Light green (inner)
        ]
        
        for i, color in enumerate(head_colors):
            width = head_width - i * 2
            height = head_height - i * 2
            if width > 0 and height > 0:
                head_rect = pygame.Rect(
                    center_x - width // 2,
                    center_y - height // 2,
                    width,
                    height
                )
                pygame.draw.ellipse(self.screen, color, head_rect)
        
        # Draw realistic eyes
        self._draw_snake_eyes(center_x, center_y, direction)
        
        # Draw flickering tongue
        self._draw_snake_tongue(center_x, center_y, direction)
        
        # Add nostril details
        self._draw_snake_nostrils(center_x, center_y, direction)
    
    def _draw_snake_eyes(self, center_x: int, center_y: int, direction: Direction):
        """Draw realistic snake eyes with proper positioning.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        eye_size = 4
        pupil_size = 2
        
        # Position eyes based on direction
        if direction == Direction.RIGHT:
            eye1_pos = (center_x + 4, center_y - 4)
            eye2_pos = (center_x + 4, center_y + 4)
        elif direction == Direction.LEFT:
            eye1_pos = (center_x - 4, center_y - 4)
            eye2_pos = (center_x - 4, center_y + 4)
        elif direction == Direction.UP:
            eye1_pos = (center_x - 4, center_y - 4)
            eye2_pos = (center_x + 4, center_y - 4)
        else:  # DOWN
            eye1_pos = (center_x - 4, center_y + 4)
            eye2_pos = (center_x + 4, center_y + 4)
        
        # Draw eyes with realistic colors
        for eye_pos in [eye1_pos, eye2_pos]:
            # Eye white
            pygame.draw.circle(self.screen, (255, 255, 200), eye_pos, eye_size)
            # Eye iris (yellow-green)
            pygame.draw.circle(self.screen, (200, 255, 100), eye_pos, eye_size - 1)
            # Vertical pupil (like real snakes)
            pupil_rect = pygame.Rect(eye_pos[0] - 1, eye_pos[1] - pupil_size, 2, pupil_size * 2)
            pygame.draw.ellipse(self.screen, (0, 0, 0), pupil_rect)
            # Eye shine
            pygame.draw.circle(self.screen, (255, 255, 255), (eye_pos[0] - 1, eye_pos[1] - 1), 1)
    
    def _draw_snake_tongue(self, center_x: int, center_y: int, direction: Direction):
        """Draw a flickering forked tongue.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        # Tongue flickers based on time
        time_ms = pygame.time.get_ticks()
        tongue_visible = (time_ms // 300) % 3 != 0  # Flicker pattern
        
        if not tongue_visible:
            return
        
        tongue_length = 10
        tongue_color = (220, 20, 60)  # Red tongue
        
        # Position tongue based on direction
        if direction == Direction.RIGHT:
            tongue_start = (center_x + 8, center_y)
            tongue_end = (center_x + 8 + tongue_length, center_y)
            fork1_end = (center_x + 8 + tongue_length, center_y - 2)
            fork2_end = (center_x + 8 + tongue_length, center_y + 2)
        elif direction == Direction.LEFT:
            tongue_start = (center_x - 8, center_y)
            tongue_end = (center_x - 8 - tongue_length, center_y)
            fork1_end = (center_x - 8 - tongue_length, center_y - 2)
            fork2_end = (center_x - 8 - tongue_length, center_y + 2)
        elif direction == Direction.UP:
            tongue_start = (center_x, center_y - 8)
            tongue_end = (center_x, center_y - 8 - tongue_length)
            fork1_end = (center_x - 2, center_y - 8 - tongue_length)
            fork2_end = (center_x + 2, center_y - 8 - tongue_length)
        else:  # DOWN
            tongue_start = (center_x, center_y + 8)
            tongue_end = (center_x, center_y + 8 + tongue_length)
            fork1_end = (center_x - 2, center_y + 8 + tongue_length)
            fork2_end = (center_x + 2, center_y + 8 + tongue_length)
        
        # Draw main tongue
        pygame.draw.line(self.screen, tongue_color, tongue_start, tongue_end, 2)
        
        # Draw forked tip
        pygame.draw.line(self.screen, tongue_color, tongue_end, fork1_end, 1)
        pygame.draw.line(self.screen, tongue_color, tongue_end, fork2_end, 1)
    
    def _draw_snake_nostrils(self, center_x: int, center_y: int, direction: Direction):
        """Draw small nostril details.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        nostril_color = (20, 80, 20)  # Dark green
        
        # Position nostrils based on direction
        if direction == Direction.RIGHT:
            nostril1_pos = (center_x + 6, center_y - 2)
            nostril2_pos = (center_x + 6, center_y + 2)
        elif direction == Direction.LEFT:
            nostril1_pos = (center_x - 6, center_y - 2)
            nostril2_pos = (center_x - 6, center_y + 2)
        elif direction == Direction.UP:
            nostril1_pos = (center_x - 2, center_y - 6)
            nostril2_pos = (center_x + 2, center_y - 6)
        else:  # DOWN
            nostril1_pos = (center_x - 2, center_y + 6)
            nostril2_pos = (center_x + 2, center_y + 6)
        
        # Draw tiny nostrils
        pygame.draw.circle(self.screen, nostril_color, nostril1_pos, 1)
        pygame.draw.circle(self.screen, nostril_color, nostril2_pos, 1)
    
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
            image_rect.center = (screen_x + GameConstants.CELL_SIZE // 2, 
                               screen_y + GameConstants.CELL_SIZE // 2)
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
        
        name = fruit.name
        
        if name == "apple":
            # Enhanced apple - more emoji-like
            pygame.draw.circle(self.screen, (220, 20, 20), (center_x, center_y + 1), 9)
            pygame.draw.circle(self.screen, (255, 50, 50), (center_x - 2, center_y - 1), 7)
            pygame.draw.rect(self.screen, (101, 67, 33), (center_x - 1, screen_y + 3, 2, 5))
            pygame.draw.ellipse(self.screen, (34, 139, 34), (center_x + 1, screen_y + 3, 6, 3))
            pygame.draw.circle(self.screen, (255, 200, 200), (center_x - 3, center_y - 2), 2)
        
        elif name == "pear":
            # Enhanced pear - more emoji-like
            pygame.draw.circle(self.screen, (255, 255, 100), (center_x, center_y + 3), 7)
            pygame.draw.circle(self.screen, (200, 255, 100), (center_x, center_y - 1), 5)
            pygame.draw.rect(self.screen, (101, 67, 33), (center_x - 1, screen_y + 3, 2, 4))
            pygame.draw.circle(self.screen, (255, 255, 200), (center_x - 2, center_y), 2)
        
        elif name == "banana":
            # Enhanced banana - more emoji-like curved shape
            points = [
                (center_x - 7, center_y + 3),
                (center_x - 5, center_y - 7),
                (center_x + 1, center_y - 6),
                (center_x + 7, center_y + 5),
                (center_x + 4, center_y + 7),
                (center_x - 4, center_y + 5)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 0), points)
            pygame.draw.circle(self.screen, (101, 67, 33), (center_x - 5, center_y - 7), 2)
            pygame.draw.line(self.screen, (200, 200, 0), (center_x - 4, center_y - 4), (center_x + 3, center_y + 3), 1)
            pygame.draw.line(self.screen, (200, 200, 0), (center_x - 2, center_y - 5), (center_x + 5, center_y + 2), 1)
        
        elif name == "cherry":
            # Enhanced cherries - more emoji-like
            pygame.draw.circle(self.screen, (139, 0, 0), (center_x - 3, center_y + 2), 6)
            pygame.draw.circle(self.screen, (220, 20, 60), (center_x - 3, center_y + 2), 5)
            pygame.draw.circle(self.screen, (139, 0, 0), (center_x + 3, center_y + 3), 6)
            pygame.draw.circle(self.screen, (220, 20, 60), (center_x + 3, center_y + 3), 5)
            pygame.draw.line(self.screen, (34, 139, 34), (center_x - 3, center_y - 4), (center_x - 1, center_y - 7), 2)
            pygame.draw.line(self.screen, (34, 139, 34), (center_x + 3, center_y - 3), (center_x + 1, center_y - 7), 2)
            pygame.draw.circle(self.screen, (255, 100, 100), (center_x - 4, center_y + 1), 2)
            pygame.draw.circle(self.screen, (255, 100, 100), (center_x + 2, center_y + 2), 2)
        
        elif name == "orange":
            # Enhanced orange - more emoji-like with texture
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
