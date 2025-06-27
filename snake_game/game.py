"""Snake Game Implementation with Pygame."""

import pygame
import random
import json
import os
from enum import Enum
from typing import List, Tuple, Optional


class Direction(Enum):
    """Direction enumeration for snake movement."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameState(Enum):
    """Game state enumeration."""
    SPLASH = "splash"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    HIGH_SCORES = "high_scores"


class SnakeGame:
    """Main Snake Game class."""
    
    # Game constants
    GRID_WIDTH = 40
    GRID_HEIGHT = 30
    CELL_SIZE = 20
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    DARK_GREEN = (0, 128, 0)
    GRAY = (128, 128, 128)
    
    # Initial game settings
    INITIAL_SNAKE_LENGTH = 5
    INITIAL_SPEED = 200  # milliseconds between moves
    SPEED_INCREASE = 10  # speed increase per fruit eaten
    POINTS_PER_FRUIT = 4
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = GameState.SPLASH
        self.score = 0
        self.snake = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.fruit_pos = (0, 0)
        self.speed = self.INITIAL_SPEED
        self.last_move_time = 0
        self.high_scores = self.load_high_scores()
        
        # Sound effects (we'll create simple tones)
        self.create_sound_effects()
        
        self.reset_game()
    
    def create_sound_effects(self):
        """Create sound effects for the game."""
        try:
            # Create simple sound effects using pygame's sound generation
            self.eat_sound = pygame.mixer.Sound(buffer=self.generate_tone(440, 0.1))
            self.game_over_sound = pygame.mixer.Sound(buffer=self.generate_tone(220, 0.5))
            self.move_sound = pygame.mixer.Sound(buffer=self.generate_tone(880, 0.05))
        except:
            # Fallback if sound generation fails
            self.eat_sound = None
            self.game_over_sound = None
            self.move_sound = None
    
    def generate_tone(self, frequency: float, duration: float) -> bytes:
        """Generate a simple tone for sound effects."""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2), dtype=np.int16)
        
        # Generate sine wave
        for i in range(frames):
            wave = int(16383 * np.sin(2 * np.pi * frequency * i / sample_rate))
            arr[i] = [wave, wave]
        
        return arr.tobytes()
    
    def load_high_scores(self) -> List[int]:
        """Load high scores from file."""
        scores_file = "high_scores.json"
        try:
            if os.path.exists(scores_file):
                with open(scores_file, 'r') as f:
                    scores = json.load(f)
                    return sorted(scores, reverse=True)[:5]
        except:
            pass
        return [0, 0, 0, 0, 0]
    
    def save_high_scores(self):
        """Save high scores to file."""
        scores_file = "high_scores.json"
        try:
            with open(scores_file, 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def update_high_scores(self, score: int):
        """Update high scores list with new score."""
        self.high_scores.append(score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]
        self.save_high_scores()
    
    def reset_game(self):
        """Reset the game to initial state."""
        # Initialize snake in the center
        center_x = self.GRID_WIDTH // 2
        center_y = self.GRID_HEIGHT // 2
        
        self.snake = []
        for i in range(self.INITIAL_SNAKE_LENGTH):
            self.snake.append((center_x - i, center_y))
        
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.speed = self.INITIAL_SPEED
        self.spawn_fruit()
    
    def spawn_fruit(self):
        """Spawn a new fruit at a random location not occupied by the snake."""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.fruit_pos = (x, y)
                break
    
    def handle_input(self, event):
        """Handle keyboard input."""
        if event.type == pygame.KEYDOWN:
            if self.state == GameState.SPLASH:
                self.state = GameState.PLAYING
                self.last_move_time = pygame.time.get_ticks()
            
            elif self.state == GameState.PLAYING:
                # Handle direction changes
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
            
            elif self.state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = GameState.PLAYING
                    self.last_move_time = pygame.time.get_ticks()
                elif event.key == pygame.K_h:
                    self.state = GameState.HIGH_SCORES
            
            elif self.state == GameState.HIGH_SCORES:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = GameState.PLAYING
                    self.last_move_time = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.SPLASH
    
    def update_game(self):
        """Update game logic."""
        if self.state != GameState.PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.speed:
            self.move_snake()
            self.last_move_time = current_time
    
    def move_snake(self):
        """Move the snake and handle game logic."""
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT):
            self.game_over()
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over()
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check fruit collision
        if new_head == self.fruit_pos:
            self.eat_fruit()
        else:
            # Remove tail if no fruit eaten
            self.snake.pop()
        
        # Play move sound (with increasing frequency for urgency)
        if self.move_sound and len(self.snake) > self.INITIAL_SNAKE_LENGTH:
            # Increase pitch based on snake length
            urgency_factor = min(len(self.snake) / 20.0, 2.0)
            try:
                # Create a higher pitched sound for urgency
                urgent_sound = pygame.mixer.Sound(buffer=self.generate_tone(880 * urgency_factor, 0.03))
                urgent_sound.set_volume(0.3)
                urgent_sound.play()
            except:
                pass
    
    def eat_fruit(self):
        """Handle fruit eating logic."""
        self.score += self.POINTS_PER_FRUIT
        self.speed = max(50, self.speed - self.SPEED_INCREASE)  # Increase speed, minimum 50ms
        self.spawn_fruit()
        
        # Play eat sound with increasing urgency
        if self.eat_sound:
            try:
                # Higher pitch for longer snakes
                urgency_factor = 1 + (len(self.snake) / 30.0)
                urgent_eat_sound = pygame.mixer.Sound(buffer=self.generate_tone(440 * urgency_factor, 0.15))
                urgent_eat_sound.set_volume(0.5)
                urgent_eat_sound.play()
            except:
                pass
    
    def game_over(self):
        """Handle game over."""
        self.state = GameState.GAME_OVER
        self.update_high_scores(self.score)
        
        # Play game over sound
        if self.game_over_sound:
            self.game_over_sound.set_volume(0.7)
            self.game_over_sound.play()
    
    def draw_splash_screen(self):
        """Draw the splash screen."""
        self.screen.fill(self.BLACK)
        
        # Title
        title_text = self.font.render("SNAKE GAME", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Use arrow keys to control the snake",
            "Eat the red fruit to grow and score points",
            "Avoid hitting walls and yourself",
            "Each fruit gives 4 points and increases speed",
            "",
            "Press any key to start!"
        ]
        
        y_offset = 250
        for instruction in instructions:
            if instruction:  # Skip empty lines
                text = self.small_font.render(instruction, True, self.WHITE)
                text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_game(self):
        """Draw the game screen."""
        self.screen.fill(self.BLACK)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, 
                             self.CELL_SIZE, self.CELL_SIZE)
            
            # Head is brighter green
            color = self.GREEN if i == 0 else self.DARK_GREEN
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 1)
        
        # Draw fruit
        fruit_x, fruit_y = self.fruit_pos
        fruit_rect = pygame.Rect(fruit_x * self.CELL_SIZE, fruit_y * self.CELL_SIZE,
                               self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, self.RED, fruit_rect)
        
        # Draw score
        score_text = self.small_font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw length
        length_text = self.small_font.render(f"Length: {len(self.snake)}", True, self.WHITE)
        self.screen.blit(length_text, (10, 35))
    
    def draw_game_over_screen(self):
        """Draw the game over screen."""
        self.screen.fill(self.BLACK)
        
        # Game Over title
        game_over_text = self.font.render("GAME OVER!", True, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Check if it's a high score
        if self.score in self.high_scores[:5]:
            high_score_text = self.small_font.render("NEW HIGH SCORE!", True, self.YELLOW)
            high_score_rect = high_score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 230))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press H to view high scores"
        ]
        
        y_offset = 300
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_high_scores_screen(self):
        """Draw the high scores screen."""
        self.screen.fill(self.BLACK)
        
        # Title
        title_text = self.font.render("HIGH SCORES", True, self.YELLOW)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # High scores
        y_offset = 180
        for i, score in enumerate(self.high_scores):
            score_text = self.small_font.render(f"{i + 1}. {score}", True, self.WHITE)
            score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(score_text, score_rect)
            y_offset += 40
        
        # Instructions
        instructions = [
            "Press SPACE to play again",
            "Press ESC to return to splash screen"
        ]
        
        y_offset = 450
        for instruction in instructions:
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw(self):
        """Draw the current game state."""
        if self.state == GameState.SPLASH:
            self.draw_splash_screen()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen()
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)
            
            self.update_game()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
