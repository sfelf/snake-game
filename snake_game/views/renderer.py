"""Game renderer for the Snake Game."""

import pygame
import math
from typing import List, Tuple
from ..models import Snake, Fruit, GameState, FruitType, Direction
from ..utils import GameConstants
from ..utils.path_smoother import PathSmoother
from .snake_renderer import SnakeBodyRenderer, SnakeHeadRenderer, SnakeScaleRenderer


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
        """Create a completely smooth path through the snake segments with proper head handling.
        
        Args:
            points: List of screen coordinate points
            
        Returns:
            List of smoothed points for drawing
        """
        if len(points) < 2:
            return points
        
        if len(points) == 2:
            # For short snake, interpolate between head and tail
            return self._interpolate_points(points[0], points[1], 8)
        
        smooth_points = []
        
        # Start with head - ensure smooth start
        smooth_points.append(points[0])
        
        # Handle first segment specially to avoid head humpback
        if len(points) > 2:
            # Smooth transition from head to first body segment
            head_to_first = self._interpolate_points(points[0], points[1], 10)
            smooth_points.extend(head_to_first[1:])  # Skip first point (already added)
        
        # Create smooth curves between remaining segments
        for i in range(1, len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            
            # Get context points for better curve calculation
            prev_point = points[i - 1] if i > 0 else None
            next_point = points[i + 2] if i + 2 < len(points) else None
            
            # Create smooth interpolation between segments
            if i == len(points) - 2:  # Last segment
                # Simple interpolation to tail
                interpolated = self._interpolate_points(start_point, end_point, 8)
                smooth_points.extend(interpolated[1:])  # Skip first point (already added)
            else:
                # Create curved path considering neighboring segments
                # Reduce curve intensity near head to prevent humpback
                curve_intensity = min(1.0, i / 3.0)  # Gradual curve increase from head
                curved_points = self._create_curved_segment(start_point, end_point, prev_point, next_point, curve_intensity)
                smooth_points.extend(curved_points[1:])  # Skip first point (already added)
        
        return smooth_points
    
    def _interpolate_points(self, start_point, end_point, num_points):
        """Create smooth interpolation between two points.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            num_points: Number of interpolation points
            
        Returns:
            List of interpolated points
        """
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            x = int(start_point[0] + (end_point[0] - start_point[0]) * t)
            y = int(start_point[1] + (end_point[1] - start_point[1]) * t)
            points.append((x, y))
        return points
    
    def _create_curved_segment(self, start_point, end_point, prev_point, next_point, curve_intensity=1.0):
        """Create a curved segment with enhanced smoothness and controlled arcing.
        
        Args:
            start_point: Current segment start
            end_point: Current segment end
            prev_point: Previous segment (for curve context)
            next_point: Next segment (for curve context)
            curve_intensity: Intensity of curve (0.0 to 1.0) to control near-head smoothness
            
        Returns:
            List of points forming an ultra-smooth curve
        """
        # Increased interpolation points for maximum smoothness
        num_points = 16  # Increased from 12 for ultra-smooth curves
        curve_points = []
        
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Use enhanced Catmull-Rom spline for ultra-smooth curves
            if prev_point and next_point:
                # Full spline with 4 control points and tension adjustment
                point = self._enhanced_catmull_rom_spline(prev_point, start_point, end_point, next_point, t)
            else:
                # Enhanced interpolation with controlled curve bias
                # Create more pronounced arc but controlled by curve_intensity
                mid_x = (start_point[0] + end_point[0]) / 2
                mid_y = (start_point[1] + end_point[1]) / 2
                
                # Enhanced curve factor with intensity control
                base_curve_factor = 0.4 * math.sin(t * math.pi)
                curve_factor = base_curve_factor * curve_intensity  # Apply intensity control
                
                # Perpendicular offset for enhanced curve
                dx = end_point[0] - start_point[0]
                dy = end_point[1] - start_point[1]
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    perp_x = -dy / length * curve_factor * 15  # Curve strength
                    perp_y = dx / length * curve_factor * 15
                else:
                    perp_x = perp_y = 0
                
                x = int(start_point[0] + (end_point[0] - start_point[0]) * t + perp_x)
                y = int(start_point[1] + (end_point[1] - start_point[1]) * t + perp_y)
                point = (x, y)
            
            curve_points.append(point)
        
        return curve_points
    
    def _enhanced_catmull_rom_spline(self, p0, p1, p2, p3, t):
        """Calculate enhanced Catmull-Rom spline with tension control for ultra-smooth curves.
        
        Args:
            p0, p1, p2, p3: Control points
            t: Parameter (0 to 1)
            
        Returns:
            Interpolated point (x, y)
        """
        # Enhanced tension parameter for smoother curves
        tension = 0.5  # Standard Catmull-Rom tension
        
        t2 = t * t
        t3 = t2 * t
        
        # Enhanced Catmull-Rom spline formula with tension
        x = tension * ((2 * p1[0]) +
                      (-p0[0] + p2[0]) * t +
                      (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                      (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        
        y = tension * ((2 * p1[1]) +
                      (-p0[1] + p2[1]) * t +
                      (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                      (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        
        return (int(x), int(y))
    
    def _draw_smooth_snake_body(self, points: list, segments: list):
        """Draw the snake body with proper proportions and green striped coloring.
        
        Args:
            points: Smoothed path points
            segments: Original segment positions for thickness calculation
        """
        if len(points) < 2:
            return
        
        # Draw the snake body with proper proportions and green stripes
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            
            # Calculate proper body proportions: thinner at head, widest in middle, tapered to tail
            progress = i / max(1, len(points) - 1)
            
            # Create natural body thickness curve
            if progress < 0.3:  # Head section - thinner
                thickness_factor = 0.7 + (progress / 0.3) * 0.3  # 0.7 to 1.0
            elif progress < 0.7:  # Middle section - widest
                middle_progress = (progress - 0.3) / 0.4
                thickness_factor = 1.0 + math.sin(middle_progress * math.pi) * 0.3  # 1.0 to 1.3 and back
            else:  # Tail section - tapered
                tail_progress = (progress - 0.7) / 0.3
                thickness_factor = 1.0 - tail_progress * 0.6  # 1.0 to 0.4
            
            base_thickness = 16  # Base thickness
            thickness = max(4, int(base_thickness * thickness_factor))
            
            # Draw enhanced segment with proper proportions and stripes
            self._draw_striped_segment(start_point, end_point, thickness, progress, i)
    
    def _draw_striped_segment(self, start_point, end_point, thickness, progress, segment_index):
        """Draw a single segment with green coloring and stripe patterns.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            thickness: Segment thickness
            progress: Position along snake (0=head, 1=tail)
            segment_index: Index for stripe patterns
        """
        # Calculate segment direction
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
        
        # Enhanced green coloration with shimmer
        base_intensity = 1.0 - progress * 0.1  # Less fade for better visibility
        
        # Multi-wave shimmer system
        time_ms = pygame.time.get_ticks()
        primary_shimmer = math.sin((time_ms * 0.003) + (segment_index * 0.2)) * 0.3 + 0.7
        secondary_shimmer = math.cos((time_ms * 0.002) + (segment_index * 0.15)) * 0.2 + 0.8
        shimmer_intensity = (primary_shimmer * secondary_shimmer) * base_intensity
        
        # Stripe pattern - every few segments gets darker stripes
        stripe_pattern = math.sin(segment_index * 0.4) > 0.3  # Creates stripe bands
        stripe_intensity = 0.7 if stripe_pattern else 1.0
        
        # Green coloration with stripes
        base_colors = {
            'shadow': (int(8 * base_intensity * stripe_intensity), int(35 * base_intensity * stripe_intensity), int(8 * base_intensity * stripe_intensity)),
            'main_shadow': (int(18 * base_intensity * stripe_intensity), int(70 * base_intensity * stripe_intensity), int(18 * base_intensity * stripe_intensity)),
            'secondary': (int(25 * base_intensity * stripe_intensity), int(90 * base_intensity * stripe_intensity), int(25 * base_intensity * stripe_intensity)),
            'base': (int(40 * base_intensity * stripe_intensity), int(140 * base_intensity * stripe_intensity), int(40 * base_intensity * stripe_intensity)),
            'mid': (int(50 * shimmer_intensity * stripe_intensity), int(170 * shimmer_intensity * stripe_intensity), int(50 * shimmer_intensity * stripe_intensity)),
            'highlight': (int(65 * shimmer_intensity * stripe_intensity), int(210 * shimmer_intensity * stripe_intensity), int(65 * shimmer_intensity * stripe_intensity)),
            'top': (int(85 * shimmer_intensity * stripe_intensity), int(240 * shimmer_intensity * stripe_intensity), int(85 * shimmer_intensity * stripe_intensity)),
            'specular': (int(110 * shimmer_intensity * stripe_intensity), int(255 * shimmer_intensity * stripe_intensity), int(110 * shimmer_intensity * stripe_intensity)),
            'ultra': (int(140 * shimmer_intensity * stripe_intensity), int(255 * shimmer_intensity * stripe_intensity), int(140 * shimmer_intensity * stripe_intensity))
        }
        
        # Enhanced 9-layer shading system with green striped colors
        shading_layers = [
            # Deep shadow
            {
                'color': base_colors['shadow'],
                'offset': (-0.3, -0.3),
                'thickness_mult': 1.05,
                'blur': True
            },
            # Main shadow layer
            {
                'color': base_colors['main_shadow'],
                'offset': (-0.2, -0.2),
                'thickness_mult': 1.0,
                'blur': False
            },
            # Secondary shadow
            {
                'color': base_colors['secondary'],
                'offset': (-0.1, -0.1),
                'thickness_mult': 0.98,
                'blur': False
            },
            # Base body color
            {
                'color': base_colors['base'],
                'offset': (0, 0),
                'thickness_mult': 0.95,
                'blur': False
            },
            # Mid-tone with shimmer
            {
                'color': base_colors['mid'],
                'offset': (0.05, 0.05),
                'thickness_mult': 0.8,
                'blur': False
            },
            # Bright highlight
            {
                'color': base_colors['highlight'],
                'offset': (0.12, 0.12),
                'thickness_mult': 0.65,
                'blur': False
            },
            # Top highlight
            {
                'color': base_colors['top'],
                'offset': (0.18, 0.18),
                'thickness_mult': 0.45,
                'blur': False
            },
            # Specular highlight
            {
                'color': base_colors['specular'],
                'offset': (0.22, 0.22),
                'thickness_mult': 0.25,
                'blur': False
            },
            # Ultra-bright specular
            {
                'color': base_colors['ultra'],
                'offset': (0.25, 0.25),
                'thickness_mult': 0.12,
                'blur': False
            }
        ]
        
        # Draw each shading layer
        for layer in shading_layers:
            layer_thickness = max(1, int(thickness * layer['thickness_mult']))
            
            # Enhanced offset calculation
            offset_scale = min(1.0, thickness / 16.0)  # Normalize to base thickness
            offset_distance = thickness * 0.08 * offset_scale
            
            offset_x = layer['offset'][0] * offset_distance
            offset_y = layer['offset'][1] * offset_distance
            
            offset_start = (int(start_point[0] + offset_x), int(start_point[1] + offset_y))
            offset_end = (int(end_point[0] + offset_x), int(end_point[1] + offset_y))
            
            # Draw the layer
            if layer.get('blur', False):
                self._draw_blurred_line(offset_start, offset_end, layer['color'], layer_thickness)
            else:
                self._draw_ultra_smooth_line(offset_start, offset_end, layer['color'], layer_thickness)
    
    def _draw_enhanced_3d_segment(self, start_point, end_point, thickness, progress, segment_index):
        """Draw a single segment with python coloration and maximum 3D effects.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            thickness: Segment thickness
            progress: Position along snake (0=head, 1=tail)
            segment_index: Index for shimmer animation
        """
        # Calculate segment direction for proper lighting simulation
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
        
        # Enhanced color progression with python coloration
        base_intensity = 1.0 - progress * 0.15  # Less fade for better visibility
        
        # Multi-wave shimmer system for more complex lighting
        time_ms = pygame.time.get_ticks()
        primary_shimmer = math.sin((time_ms * 0.003) + (segment_index * 0.2)) * 0.3 + 0.7
        secondary_shimmer = math.cos((time_ms * 0.002) + (segment_index * 0.15)) * 0.2 + 0.8
        shimmer_intensity = (primary_shimmer * secondary_shimmer) * base_intensity
        
        # Python pattern variation - create banded pattern
        pattern_wave = math.sin(segment_index * 0.8) * 0.3 + 0.7
        is_dark_band = (segment_index // 3) % 2 == 0  # Alternating bands every 3 segments
        
        # Python coloration - browns and tans with pattern
        if is_dark_band:
            # Dark brown bands
            base_colors = {
                'shadow': (int(15 * base_intensity), int(10 * base_intensity), int(5 * base_intensity)),
                'main_shadow': (int(25 * base_intensity), int(18 * base_intensity), int(10 * base_intensity)),
                'secondary': (int(35 * base_intensity), int(25 * base_intensity), int(15 * base_intensity)),
                'base': (int(60 * base_intensity), int(45 * base_intensity), int(25 * base_intensity)),
                'mid': (int(80 * shimmer_intensity), int(60 * shimmer_intensity), int(35 * shimmer_intensity)),
                'highlight': (int(100 * shimmer_intensity), int(80 * shimmer_intensity), int(50 * shimmer_intensity)),
                'top': (int(120 * shimmer_intensity), int(100 * shimmer_intensity), int(70 * shimmer_intensity)),
                'specular': (int(140 * shimmer_intensity), int(120 * shimmer_intensity), int(90 * shimmer_intensity)),
                'ultra': (int(160 * shimmer_intensity), int(140 * shimmer_intensity), int(110 * shimmer_intensity))
            }
        else:
            # Light tan/cream bands
            base_colors = {
                'shadow': (int(25 * base_intensity), int(20 * base_intensity), int(15 * base_intensity)),
                'main_shadow': (int(45 * base_intensity), int(35 * base_intensity), int(25 * base_intensity)),
                'secondary': (int(65 * base_intensity), int(50 * base_intensity), int(35 * base_intensity)),
                'base': (int(100 * base_intensity), int(80 * base_intensity), int(55 * base_intensity)),
                'mid': (int(130 * shimmer_intensity), int(110 * shimmer_intensity), int(80 * shimmer_intensity)),
                'highlight': (int(160 * shimmer_intensity), int(140 * shimmer_intensity), int(110 * shimmer_intensity)),
                'top': (int(180 * shimmer_intensity), int(160 * shimmer_intensity), int(130 * shimmer_intensity)),
                'specular': (int(200 * shimmer_intensity), int(180 * shimmer_intensity), int(150 * shimmer_intensity)),
                'ultra': (int(220 * shimmer_intensity), int(200 * shimmer_intensity), int(170 * shimmer_intensity))
            }
        
        # Enhanced 9-layer shading system with python colors
        shading_layers = [
            # Deep shadow (simulates ambient occlusion)
            {
                'color': base_colors['shadow'],
                'offset': (-0.3, -0.3),
                'thickness_mult': 1.05,
                'blur': True
            },
            # Main shadow layer
            {
                'color': base_colors['main_shadow'],
                'offset': (-0.2, -0.2),
                'thickness_mult': 1.0,
                'blur': False
            },
            # Secondary shadow
            {
                'color': base_colors['secondary'],
                'offset': (-0.1, -0.1),
                'thickness_mult': 0.98,
                'blur': False
            },
            # Base body color (main surface)
            {
                'color': base_colors['base'],
                'offset': (0, 0),
                'thickness_mult': 0.95,
                'blur': False
            },
            # Mid-tone with primary shimmer
            {
                'color': base_colors['mid'],
                'offset': (0.05, 0.05),
                'thickness_mult': 0.8,
                'blur': False
            },
            # Bright highlight with shimmer
            {
                'color': base_colors['highlight'],
                'offset': (0.12, 0.12),
                'thickness_mult': 0.65,
                'blur': False
            },
            # Top highlight (simulates direct lighting)
            {
                'color': base_colors['top'],
                'offset': (0.18, 0.18),
                'thickness_mult': 0.45,
                'blur': False
            },
            # Specular highlight (surface reflection)
            {
                'color': base_colors['specular'],
                'offset': (0.22, 0.22),
                'thickness_mult': 0.25,
                'blur': False
            },
            # Ultra-bright specular (wet python effect)
            {
                'color': base_colors['ultra'],
                'offset': (0.25, 0.25),
                'thickness_mult': 0.12,
                'blur': False
            }
        ]
        
        # Draw each shading layer with enhanced 3D positioning
        for layer in shading_layers:
            layer_thickness = max(1, int(thickness * layer['thickness_mult']))
            
            # Enhanced offset calculation for maximum 3D effect
            offset_scale = min(1.0, thickness / 18.0)  # Normalize to base thickness
            offset_distance = thickness * 0.08 * offset_scale  # Fine-tuned for realism
            
            offset_x = layer['offset'][0] * offset_distance
            offset_y = layer['offset'][1] * offset_distance
            
            offset_start = (int(start_point[0] + offset_x), int(start_point[1] + offset_y))
            offset_end = (int(end_point[0] + offset_x), int(end_point[1] + offset_y))
            
            # Draw the layer with maximum smoothness
            if layer.get('blur', False):
                # Draw blurred shadow for ambient occlusion effect
                self._draw_blurred_line(offset_start, offset_end, layer['color'], layer_thickness)
            else:
                self._draw_ultra_smooth_line(offset_start, offset_end, layer['color'], layer_thickness)
    
    def _draw_blurred_line(self, start_point, end_point, color, thickness):
        """Draw a blurred line for shadow effects.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            color: Line color
            thickness: Line thickness
        """
        if thickness <= 0:
            return
        
        # Create multiple offset lines for blur effect
        blur_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        blur_color = tuple(c // 2 for c in color[:3])  # Darker for blur
        
        # Draw blur layers
        for offset_x, offset_y in blur_offsets:
            blur_start = (start_point[0] + offset_x, start_point[1] + offset_y)
            blur_end = (end_point[0] + offset_x, end_point[1] + offset_y)
            
            if thickness > 1:
                pygame.draw.line(self.screen, blur_color, blur_start, blur_end, max(1, thickness - 1))
        
        # Draw main line
        self._draw_ultra_smooth_line(start_point, end_point, color, thickness)
    
    def _draw_ultra_smooth_line(self, start_point, end_point, color, thickness):
        """Draw an ultra-smooth thick line with perfect anti-aliasing.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            color: Line color
            thickness: Line thickness
        """
        if thickness <= 0:
            return
        
        # For very smooth lines, draw multiple thin lines with slight offsets
        if thickness > 4:
            # Draw main thick line
            pygame.draw.line(self.screen, color, start_point, end_point, thickness)
            
            # Add anti-aliasing by drawing thinner lines around the edges
            edge_color = tuple(min(255, c + 20) for c in color[:3])
            pygame.draw.line(self.screen, edge_color, start_point, end_point, max(1, thickness - 2))
            
            # Draw perfect rounded end caps
            radius = thickness // 2
            if radius > 0:
                # Main caps
                pygame.draw.circle(self.screen, color, start_point, radius)
                pygame.draw.circle(self.screen, color, end_point, radius)
                
                # Anti-aliased edge caps
                if radius > 2:
                    pygame.draw.circle(self.screen, edge_color, start_point, radius - 1)
                    pygame.draw.circle(self.screen, edge_color, end_point, radius - 1)
        else:
            # For thin lines, just draw normally
            pygame.draw.line(self.screen, color, start_point, end_point, thickness)
            if thickness > 1:
                radius = thickness // 2
                pygame.draw.circle(self.screen, color, start_point, radius)
                pygame.draw.circle(self.screen, color, end_point, radius)
    
    def _draw_snake_scales(self, points: list):
        """Draw green scale patterns with stripe effects.
        
        Args:
            points: Path points along the snake body
        """
        scale_spacing = 20  # Spacing for scales
        time_ms = pygame.time.get_ticks()
        
        for i in range(0, len(points) - 1, scale_spacing):
            if i + 1 < len(points):
                point = points[i]
                
                # Calculate scale size based on position (smaller toward tail)
                progress = i / max(1, len(points) - 1)
                base_scale_size = max(2, int(4 * (1.0 - progress * 0.4)))
                
                # Shimmer effect for scales
                shimmer = math.sin((time_ms * 0.004) + (i * 0.15)) * 0.4 + 0.6
                scale_size = int(base_scale_size * shimmer)
                
                # Green scale coloring with stripe variation
                stripe_pattern = math.sin(i * 0.4) > 0.3
                stripe_intensity = 0.7 if stripe_pattern else 1.0
                
                base_green = int(80 * shimmer * stripe_intensity)
                bright_green = int(160 * shimmer * stripe_intensity)
                
                scale_alpha = int(90 * shimmer)
                scale_color = (int(base_green * 0.5), base_green, int(base_green * 0.5), scale_alpha)
                highlight_color = (int(bright_green * 0.6), bright_green, int(bright_green * 0.6), int(scale_alpha * 0.7))
                
                # Draw simple diamond scale
                scale_points = [
                    (point[0] - scale_size, point[1]),
                    (point[0], point[1] - scale_size),
                    (point[0] + scale_size, point[1]),
                    (point[0], point[1] + scale_size)
                ]
                
                # Create surface for alpha blending
                scale_surface = pygame.Surface((scale_size * 2 + 2, scale_size * 2 + 2), pygame.SRCALPHA)
                
                # Adjust points for surface coordinates
                surface_points = [(x - point[0] + scale_size + 1, y - point[1] + scale_size + 1) for x, y in scale_points]
                
                pygame.draw.polygon(scale_surface, scale_color, surface_points)
                
                # Add highlight
                if scale_size > 1:
                    highlight_points = [(x - 1, y - 1) for x, y in surface_points]
                    pygame.draw.polygon(scale_surface, highlight_color, highlight_points)
                
                self.screen.blit(scale_surface, (point[0] - scale_size - 1, point[1] - scale_size - 1))
    
    def _draw_snake_head(self, x: int, y: int, direction: Direction):
        """Draw a realistic elongated snake head with proper proportions.
        
        Args:
            x: Grid x position
            y: Grid y position
            direction: Snake's current direction
        """
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2
        
        # More elongated head dimensions
        base_width = 14
        base_height = 24  # Much more elongated
        
        # Adjust head orientation based on direction
        if direction in [Direction.LEFT, Direction.RIGHT]:
            head_width, head_height = base_height, base_width
        else:
            head_width, head_height = base_width, base_height
        
        # Draw multi-layered elongated head with green coloring
        self._draw_elongated_head_layers(center_x, center_y, head_width, head_height, direction)
        
        # Draw realistic eyes
        self._draw_snake_eyes(center_x, center_y, direction)
        
        # Draw animated forked tongue
        self._draw_snake_tongue(center_x, center_y, direction)
        
        # Draw detailed nostrils
        self._draw_enhanced_nostrils(center_x, center_y, direction)
    
    def _draw_elongated_head_layers(self, center_x: int, center_y: int, width: int, height: int, direction: Direction):
        """Draw multiple layers for elongated snake head with green coloring.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            width: Head width
            height: Head height
            direction: Snake's current direction
        """
        # Time-based shimmer for head
        time_ms = pygame.time.get_ticks()
        shimmer = math.sin(time_ms * 0.002) * 0.2 + 0.8
        
        # Green head layers with proper elongated shape
        head_layers = [
            # Deep shadow layer
            {
                'color': (int(15 * shimmer), int(60 * shimmer), int(15 * shimmer)),
                'offset': (-2, -2),
                'size_mult': 1.1,
            },
            # Main shadow layer
            {
                'color': (int(25 * shimmer), int(90 * shimmer), int(25 * shimmer)),
                'offset': (-1, -1),
                'size_mult': 1.05,
            },
            # Base head color - green
            {
                'color': (int(40 * shimmer), int(140 * shimmer), int(40 * shimmer)),
                'offset': (0, 0),
                'size_mult': 1.0,
            },
            # Mid-tone highlight
            {
                'color': (int(55 * shimmer), int(180 * shimmer), int(55 * shimmer)),
                'offset': (0, 0),
                'size_mult': 0.85,
            },
            # Bright highlight
            {
                'color': (int(70 * shimmer), int(220 * shimmer), int(70 * shimmer)),
                'offset': (1, 1),
                'size_mult': 0.7,
            },
            # Top shimmer highlight
            {
                'color': (int(90 * shimmer), int(255 * shimmer), int(90 * shimmer)),
                'offset': (2, 2),
                'size_mult': 0.5,
            }
        ]
        
        # Draw each head layer with elongated shape
        for layer in head_layers:
            layer_width = int(width * layer['size_mult'])
            layer_height = int(height * layer['size_mult'])
            
            # Apply offset for 3D effect
            offset_x = center_x + layer['offset'][0]
            offset_y = center_y + layer['offset'][1]
            
            # Create elongated head shape rectangle
            head_rect = pygame.Rect(
                offset_x - layer_width // 2,
                offset_y - layer_height // 2,
                layer_width,
                layer_height
            )
            
            # Draw elongated elliptical head shape
            pygame.draw.ellipse(self.screen, layer['color'], head_rect)
    
    def _draw_3d_head_layers(self, center_x: int, center_y: int, width: int, height: int, direction: Direction):
        """Draw multiple layers for realistic 3D python head shape with proper depth.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            width: Head width
            height: Head height
            direction: Snake's current direction
        """
        # Time-based shimmer for python head
        time_ms = pygame.time.get_ticks()
        shimmer = math.sin(time_ms * 0.002) * 0.2 + 0.8
        
        # Python head layers with characteristic brown/tan coloration
        head_layers = [
            # Deep shadow layer (bottom/back of head)
            {
                'color': (int(25 * shimmer), int(15 * shimmer), int(10 * shimmer)),  # Dark brown
                'offset': (-2, -2),
                'size_mult': 1.2,  # Larger for python's robust head
                'shape': 'ellipse'
            },
            # Main shadow layer
            {
                'color': (int(45 * shimmer), int(30 * shimmer), int(20 * shimmer)),  # Medium brown
                'offset': (-1, -1),
                'size_mult': 1.15,
                'shape': 'ellipse'
            },
            # Base head color - python brown
            {
                'color': (int(80 * shimmer), int(60 * shimmer), int(40 * shimmer)),  # Python brown
                'offset': (0, 0),
                'size_mult': 1.0,
                'shape': 'ellipse'
            },
            # Mid-tone highlight - lighter brown
            {
                'color': (int(120 * shimmer), int(90 * shimmer), int(60 * shimmer)),  # Light brown
                'offset': (0, 0),
                'size_mult': 0.85,
                'shape': 'ellipse'
            },
            # Bright highlight - tan color
            {
                'color': (int(160 * shimmer), int(130 * shimmer), int(90 * shimmer)),  # Tan
                'offset': (1, 1),
                'size_mult': 0.7,
                'shape': 'ellipse'
            },
            # Top shimmer highlight - light tan
            {
                'color': (int(200 * shimmer), int(170 * shimmer), int(120 * shimmer)),  # Light tan
                'offset': (2, 2),
                'size_mult': 0.5,
                'shape': 'ellipse'
            },
            # Specular highlight - cream color
            {
                'color': (int(220 * shimmer), int(200 * shimmer), int(160 * shimmer)),  # Cream
                'offset': (2, 2),
                'size_mult': 0.3,
                'shape': 'ellipse'
            }
        ]
        
        # Draw each head layer
        for layer in head_layers:
            layer_width = int(width * layer['size_mult'])
            layer_height = int(height * layer['size_mult'])
            
            # Apply offset for 3D effect
            offset_x = center_x + layer['offset'][0]
            offset_y = center_y + layer['offset'][1]
            
            # Create head shape rectangle
            head_rect = pygame.Rect(
                offset_x - layer_width // 2,
                offset_y - layer_height // 2,
                layer_width,
                layer_height
            )
            
            # Draw elliptical python head shape
            pygame.draw.ellipse(self.screen, layer['color'], head_rect)
    
    def _draw_snake_eyes(self, center_x: int, center_y: int, direction: Direction):
        """Draw realistic snake eyes with proper positioning.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        eye_size = 5
        pupil_width = 2
        pupil_height = 6
        
        # Position eyes based on direction for elongated head
        if direction == Direction.RIGHT:
            eye1_pos = (center_x + 6, center_y - 4)
            eye2_pos = (center_x + 6, center_y + 4)
        elif direction == Direction.LEFT:
            eye1_pos = (center_x - 6, center_y - 4)
            eye2_pos = (center_x - 6, center_y + 4)
        elif direction == Direction.UP:
            eye1_pos = (center_x - 4, center_y - 6)
            eye2_pos = (center_x + 4, center_y - 6)
        else:  # DOWN
            eye1_pos = (center_x - 4, center_y + 6)
            eye2_pos = (center_x + 4, center_y + 6)
        
        # Draw both eyes with realistic colors
        for eye_pos in [eye1_pos, eye2_pos]:
            # Eye socket shadow
            pygame.draw.circle(self.screen, (15, 60, 15), (eye_pos[0], eye_pos[1] + 1), eye_size + 1)
            
            # Eye white/sclera with slight yellow tint
            pygame.draw.circle(self.screen, (250, 250, 220), eye_pos, eye_size)
            
            # Iris with golden-green coloring
            pygame.draw.circle(self.screen, (180, 200, 60), eye_pos, eye_size - 1)
            
            # Inner iris detail
            pygame.draw.circle(self.screen, (160, 180, 40), eye_pos, eye_size - 2)
            
            # Vertical slit pupil (characteristic of snakes)
            pupil_rect = pygame.Rect(
                eye_pos[0] - pupil_width // 2,
                eye_pos[1] - pupil_height // 2,
                pupil_width,
                pupil_height
            )
            pygame.draw.ellipse(self.screen, (0, 0, 0), pupil_rect)
            
            # Eye shine/reflection for realism
            shine_pos = (eye_pos[0] - 2, eye_pos[1] - 2)
            pygame.draw.circle(self.screen, (255, 255, 255), shine_pos, 2)
            
            # Secondary smaller shine
            small_shine_pos = (eye_pos[0] + 1, eye_pos[1] - 1)
            pygame.draw.circle(self.screen, (200, 200, 200), small_shine_pos, 1)
    
    def _draw_enhanced_nostrils(self, center_x: int, center_y: int, direction: Direction):
        """Draw detailed nostrils with proper positioning and depth.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        nostril_size = 2
        nostril_color = (10, 40, 10)  # Very dark green
        
        # Enhanced nostril positioning based on direction
        if direction == Direction.RIGHT:
            nostril1_pos = (center_x + 8, center_y - 3)
            nostril2_pos = (center_x + 8, center_y + 3)
        elif direction == Direction.LEFT:
            nostril1_pos = (center_x - 8, center_y - 3)
            nostril2_pos = (center_x - 8, center_y + 3)
        elif direction == Direction.UP:
            nostril1_pos = (center_x - 3, center_y - 8)
            nostril2_pos = (center_x + 3, center_y - 8)
        else:  # DOWN
            nostril1_pos = (center_x - 3, center_y + 8)
            nostril2_pos = (center_x + 3, center_y + 8)
        
        # Draw nostrils with depth
        for nostril_pos in [nostril1_pos, nostril2_pos]:
            # Nostril shadow for depth
            pygame.draw.circle(self.screen, (5, 20, 5), (nostril_pos[0], nostril_pos[1] + 1), nostril_size)
            # Main nostril
            pygame.draw.circle(self.screen, nostril_color, nostril_pos, nostril_size)
            # Inner nostril darkness
            pygame.draw.circle(self.screen, (0, 0, 0), nostril_pos, nostril_size - 1)
    
    def _draw_head_scales(self, center_x: int, center_y: int, width: int, height: int, direction: Direction):
        """Draw detailed scale patterns on the snake head.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            width: Head width
            height: Head height
            direction: Snake's current direction
        """
        time_ms = pygame.time.get_ticks()
        shimmer = math.sin(time_ms * 0.003) * 0.3 + 0.7
        
        # Head scale positions (relative to center)
        scale_positions = [
            (-4, -6), (0, -7), (4, -6),  # Top row
            (-6, -2), (-2, -3), (2, -3), (6, -2),  # Upper middle
            (-5, 2), (0, 1), (5, 2),     # Lower middle
            (-3, 6), (3, 6)              # Bottom row
        ]
        
        # Adjust scale positions based on direction
        if direction == Direction.LEFT:
            scale_positions = [(-y, x) for x, y in scale_positions]
        elif direction == Direction.UP:
            scale_positions = [(y, -x) for x, y in scale_positions]
        elif direction == Direction.DOWN:
            scale_positions = [(-y, x) for x, y in scale_positions]
        
        # Draw individual head scales
        for rel_x, rel_y in scale_positions:
            scale_x = center_x + rel_x
            scale_y = center_y + rel_y
            
            # Scale size with shimmer effect
            scale_size = int(2 * shimmer) + 1
            
            # Scale color with shimmer
            scale_alpha = int(80 * shimmer)
            scale_color = (60, 200, 60, scale_alpha)
            
            # Create scale surface for alpha blending
            scale_surface = pygame.Surface((scale_size * 2 + 1, scale_size * 2 + 1), pygame.SRCALPHA)
            
            # Draw hexagonal scale shape
            scale_points = []
            for i in range(6):
                angle = i * math.pi / 3
                px = scale_size * math.cos(angle)
                py = scale_size * math.sin(angle)
                scale_points.append((scale_size + px, scale_size + py))
            
            pygame.draw.polygon(scale_surface, scale_color, scale_points)
            
            # Add scale highlight
            highlight_color = (100, 255, 100, int(scale_alpha * 0.6))
            highlight_points = []
            for i in range(6):
                angle = i * math.pi / 3
                px = (scale_size - 1) * math.cos(angle)
                py = (scale_size - 1) * math.sin(angle)
                highlight_points.append((scale_size + px, scale_size + py))
            
            if len(highlight_points) >= 3:
                pygame.draw.polygon(scale_surface, highlight_color, highlight_points)
            
            # Blit scale to screen
            self.screen.blit(scale_surface, (scale_x - scale_size, scale_y - scale_size))
    
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
