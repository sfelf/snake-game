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
        
        # Try to get a system font that supports emojis
        self.emoji_font = None
        self.use_emoji = False
        
        try:
            # Try to find a system font that supports emojis
            emoji_fonts = [
                'Apple Color Emoji',  # macOS
                'Segoe UI Emoji',     # Windows
                'Noto Color Emoji',   # Linux
                'Symbola',            # Fallback
            ]
            
            for font_name in emoji_fonts:
                try:
                    self.emoji_font = pygame.font.SysFont(font_name, 20)
                    # Test if emoji rendering works
                    test_surface = self.emoji_font.render("🍎", True, (255, 255, 255))
                    if test_surface.get_width() > 0:
                        self.use_emoji = True
                        break
                except:
                    continue
            
            if not self.use_emoji:
                # Fallback to default font
                self.emoji_font = pygame.font.Font(None, 24)
                
        except:
            self.emoji_font = pygame.font.Font(None, 24)
            self.use_emoji = False
    
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
            "Press R to reset high scores",
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
            "Press R to reset high scores",
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
            "Press R to reset high scores",
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
        """Draw graphics for the splash screen."""
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
        
        # Draw some decorative fruits around
        fruits = [
            (100, 200, FruitType.APPLE),
            (GameConstants.WINDOW_WIDTH - 100, 180, FruitType.BANANA),
            (150, 350, FruitType.CHERRY),
            (GameConstants.WINDOW_WIDTH - 150, 320, FruitType.ORANGE),
            (center_x, 400, FruitType.PEAR)
        ]
        
        for x, y, fruit_type in fruits:
            self._draw_decorative_fruit(x, y, fruit_type)
    
    def _draw_decorative_fruit(self, x: int, y: int, fruit_type: FruitType):
        """Draw a decorative fruit using emoji when available for the splash screen.
        
        Args:
            x: X position
            y: Y position
            fruit_type: Type of fruit to draw
        """
        name, primary_color, secondary_color = fruit_type.value
        
        if self.use_emoji:
            # Map fruit types to emoji
            fruit_emoji_map = {
                "apple": "🍎",
                "pear": "🍐", 
                "banana": "🍌",
                "cherry": "🍒",
                "orange": "🍊"
            }
            
            emoji = fruit_emoji_map.get(name, "🍎")
            
            try:
                # Use a larger font for decorative fruits on splash screen
                large_emoji_font = pygame.font.SysFont('Apple Color Emoji', 28) if self.use_emoji else self.emoji_font
                emoji_surface = large_emoji_font.render(emoji, True, GameConstants.WHITE)
                
                # Center the emoji at the given position
                emoji_rect = emoji_surface.get_rect()
                emoji_rect.center = (x, y)
                
                self.screen.blit(emoji_surface, emoji_rect)
                return
            except:
                pass  # Fall through to custom graphics
        
        # Fallback to custom graphics
        if name == "apple":
            pygame.draw.circle(self.screen, primary_color, (x, y + 2), 12)
            pygame.draw.rect(self.screen, secondary_color, (x - 1, y - 8, 2, 6))
        elif name == "banana":
            points = [
                (x - 8, y + 3), (x - 6, y - 8), (x + 3, y - 6),
                (x + 8, y + 6), (x + 3, y + 8), (x - 6, y + 6)
            ]
            pygame.draw.polygon(self.screen, primary_color, points)
        elif name == "cherry":
            pygame.draw.circle(self.screen, primary_color, (x - 4, y + 3), 7)
            pygame.draw.circle(self.screen, primary_color, (x + 4, y + 3), 7)
        elif name == "orange":
            pygame.draw.circle(self.screen, primary_color, (x, y), 12)
        elif name == "pear":
            pygame.draw.circle(self.screen, primary_color, (x, y + 4), 8)
            pygame.draw.circle(self.screen, primary_color, (x, y - 3), 6)
    
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
        """Draw the snake with enhanced graphics.
        
        Args:
            snake: Snake object to draw
        """
        for i, segment in enumerate(snake.segments):
            x, y = segment
            is_head = (i == 0)
            self._draw_snake_segment(x, y, is_head, i, snake.direction)
    
    def _draw_snake_segment(self, x: int, y: int, is_head: bool, segment_index: int, direction: Direction):
        """Draw a single snake segment with improved graphics.
        
        Args:
            x: Grid x position
            y: Grid y position
            is_head: Whether this is the head segment
            segment_index: Index of the segment
            direction: Current direction (for head orientation)
        """
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE
        rect = pygame.Rect(screen_x, screen_y, GameConstants.CELL_SIZE, GameConstants.CELL_SIZE)
        
        if is_head:
            # Draw snake head with eyes and direction indicator
            pygame.draw.rect(self.screen, GameConstants.GREEN, rect)
            pygame.draw.rect(self.screen, GameConstants.DARK_GREEN, rect, 2)
            
            # Draw eyes based on direction
            eye_size = 3
            if direction == Direction.RIGHT:
                eye1_pos = (screen_x + 14, screen_y + 6)
                eye2_pos = (screen_x + 14, screen_y + 14)
            elif direction == Direction.LEFT:
                eye1_pos = (screen_x + 6, screen_y + 6)
                eye2_pos = (screen_x + 6, screen_y + 14)
            elif direction == Direction.UP:
                eye1_pos = (screen_x + 6, screen_y + 6)
                eye2_pos = (screen_x + 14, screen_y + 6)
            else:  # DOWN
                eye1_pos = (screen_x + 6, screen_y + 14)
                eye2_pos = (screen_x + 14, screen_y + 14)
            
            pygame.draw.circle(self.screen, GameConstants.WHITE, eye1_pos, eye_size)
            pygame.draw.circle(self.screen, GameConstants.WHITE, eye2_pos, eye_size)
            pygame.draw.circle(self.screen, GameConstants.BLACK, eye1_pos, eye_size - 1)
            pygame.draw.circle(self.screen, GameConstants.BLACK, eye2_pos, eye_size - 1)
        else:
            # Draw body segment with pattern
            base_color = GameConstants.DARK_GREEN
            if segment_index % 2 == 0:
                base_color = (0, 100, 0)  # Slightly different shade for pattern
            
            pygame.draw.rect(self.screen, base_color, rect)
            pygame.draw.rect(self.screen, GameConstants.GREEN, rect, 1)
            
            # Add small scale pattern
            center_x = screen_x + GameConstants.CELL_SIZE // 2
            center_y = screen_y + GameConstants.CELL_SIZE // 2
            pygame.draw.circle(self.screen, (0, 80, 0), (center_x, center_y), 2)
    
    def _draw_fruit(self, fruit: Fruit):
        """Draw a fruit using emoji icons when available, fallback to custom graphics.
        
        Args:
            fruit: Fruit object to draw
        """
        x, y = fruit.position
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE
        
        if self.use_emoji:
            self._draw_fruit_emoji(screen_x, screen_y, fruit.name)
        else:
            self._draw_fruit_custom(screen_x, screen_y, fruit)
    
    def _draw_fruit_emoji(self, screen_x: int, screen_y: int, fruit_name: str):
        """Draw fruit using emoji.
        
        Args:
            screen_x: Screen X position
            screen_y: Screen Y position  
            fruit_name: Name of the fruit
        """
        # Map fruit types to emoji
        fruit_emoji_map = {
            "apple": "🍎",
            "pear": "🍐", 
            "banana": "🍌",
            "cherry": "🍒",
            "orange": "🍊"
        }
        
        emoji = fruit_emoji_map.get(fruit_name, "🍎")
        
        try:
            emoji_surface = self.emoji_font.render(emoji, True, GameConstants.WHITE)
            
            # Center the emoji in the cell
            emoji_rect = emoji_surface.get_rect()
            emoji_rect.center = (screen_x + GameConstants.CELL_SIZE // 2, 
                               screen_y + GameConstants.CELL_SIZE // 2)
            
            self.screen.blit(emoji_surface, emoji_rect)
        except:
            # Fallback to custom graphics if emoji fails
            self._draw_fruit_custom_fallback(screen_x, screen_y, fruit_name)
    
    def _draw_fruit_custom(self, screen_x: int, screen_y: int, fruit: Fruit):
        """Draw fruit using custom graphics.
        
        Args:
            screen_x: Screen X position
            screen_y: Screen Y position
            fruit: Fruit object
        """
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2
        
        name = fruit.name
        primary_color = fruit.primary_color
        secondary_color = fruit.secondary_color
        
        if name == "apple":
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y + 2), 8)
            pygame.draw.rect(self.screen, secondary_color, (center_x - 1, screen_y + 2, 2, 4))
            pygame.draw.ellipse(self.screen, secondary_color, (center_x + 2, screen_y + 2, 4, 2))
        elif name == "pear":
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y + 3), 6)
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y - 2), 4)
            pygame.draw.rect(self.screen, secondary_color, (center_x - 1, screen_y + 2, 2, 3))
        elif name == "banana":
            points = [
                (center_x - 6, center_y + 2), (center_x - 4, center_y - 6),
                (center_x + 2, center_y - 4), (center_x + 6, center_y + 4),
                (center_x + 2, center_y + 6), (center_x - 4, center_y + 4)
            ]
            pygame.draw.polygon(self.screen, primary_color, points)
            pygame.draw.circle(self.screen, secondary_color, (center_x - 4, center_y - 6), 2)
        elif name == "cherry":
            pygame.draw.circle(self.screen, primary_color, (center_x - 3, center_y + 2), 5)
            pygame.draw.circle(self.screen, primary_color, (center_x + 3, center_y + 2), 5)
            pygame.draw.line(self.screen, secondary_color, 
                           (center_x - 3, center_y - 3), (center_x - 1, center_y - 6), 2)
            pygame.draw.line(self.screen, secondary_color, 
                           (center_x + 3, center_y - 3), (center_x + 1, center_y - 6), 2)
        elif name == "orange":
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y), 8)
            for i in range(3):
                for j in range(3):
                    dot_x = center_x - 4 + i * 3
                    dot_y = center_y - 4 + j * 3
                    if (dot_x - center_x) ** 2 + (dot_y - center_y) ** 2 <= 36:
                        pygame.draw.circle(self.screen, secondary_color, (dot_x, dot_y), 1)
    
    def _draw_fruit_custom_fallback(self, screen_x: int, screen_y: int, fruit_name: str):
        """Simple fallback fruit drawing.
        
        Args:
            screen_x: Screen X position
            screen_y: Screen Y position
            fruit_name: Name of the fruit
        """
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2
        
        # Simple colored circles as fallback
        color_map = {
            "apple": GameConstants.RED,
            "pear": GameConstants.YELLOW,
            "banana": GameConstants.YELLOW,
            "cherry": (220, 20, 60),
            "orange": GameConstants.ORANGE
        }
        
        color = color_map.get(fruit_name, GameConstants.RED)
        pygame.draw.circle(self.screen, color, (center_x, center_y), 8)
