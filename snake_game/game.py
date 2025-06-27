"""Snake Game Implementation with Pygame."""

import pygame
import random
import json
import os
import math
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
    CONFIRM_RESET = "confirm_reset"


class FruitType(Enum):
    """Different types of fruits."""
    APPLE = ("apple", (255, 0, 0), (0, 150, 0))  # Red with green stem
    PEAR = ("pear", (255, 255, 0), (0, 150, 0))  # Yellow with green stem
    BANANA = ("banana", (255, 255, 0), (139, 69, 19))  # Yellow with brown tip
    CHERRY = ("cherry", (220, 20, 60), (0, 150, 0))  # Dark red with green stem
    ORANGE = ("orange", (255, 165, 0), (255, 140, 0))  # Orange with darker shade


class SnakeGame:
    """Main Snake Game class."""
    
    # Game constants
    GRID_WIDTH = 40
    GRID_HEIGHT = 30
    CELL_SIZE = 20
    BORDER_WIDTH = 2
    UI_HEIGHT = 60  # Height for UI area
    WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + (BORDER_WIDTH * 2)
    WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + (BORDER_WIDTH * 2) + UI_HEIGHT
    
    # Playing area (inside border)
    PLAY_AREA_X = BORDER_WIDTH
    PLAY_AREA_Y = BORDER_WIDTH + UI_HEIGHT
    PLAY_AREA_WIDTH = GRID_WIDTH * CELL_SIZE
    PLAY_AREA_HEIGHT = GRID_HEIGHT * CELL_SIZE
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    BROWN = (139, 69, 19)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    
    # Initial game settings
    INITIAL_SNAKE_LENGTH = 5
    INITIAL_SPEED = 200  # milliseconds between moves
    SPEED_INCREASE = 10  # speed increase per fruit eaten
    POINTS_PER_FRUIT = 4
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Game state
        self.state = GameState.SPLASH
        self.score = 0
        self.snake = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.fruit_pos = (0, 0)
        self.fruit_type = FruitType.APPLE
        self.speed = self.INITIAL_SPEED
        self.last_move_time = 0
        self.high_scores = self.load_high_scores()
        self.music_playing = False
        
        # Sound and music
        self.create_sound_effects()
        self.create_background_music()
        
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
    
    def create_background_music(self):
        """Create background music."""
        try:
            # Create a simple melodic background music
            self.background_music = self.generate_melody()
            if self.background_music:
                pygame.mixer.music.load(self.background_music)
        except:
            self.background_music = None
    
    def generate_melody(self):
        """Generate a simple melodic background music."""
        try:
            import numpy as np
            
            # Simple melody notes (frequencies in Hz)
            melody = [
                262, 294, 330, 349, 392, 440, 494, 523,  # C major scale up
                523, 494, 440, 392, 349, 330, 294, 262,  # C major scale down
                330, 392, 440, 392, 330, 294, 262, 294,  # Simple melody
                330, 349, 392, 349, 330, 294, 262, 262   # Ending
            ]
            
            sample_rate = 22050
            note_duration = 0.5  # seconds per note
            frames_per_note = int(note_duration * sample_rate)
            total_frames = len(melody) * frames_per_note
            
            # Create the audio array
            audio_data = np.zeros((total_frames, 2), dtype=np.int16)
            
            for i, freq in enumerate(melody):
                start_frame = i * frames_per_note
                end_frame = start_frame + frames_per_note
                
                # Generate sine wave for this note
                for j in range(frames_per_note):
                    if j < frames_per_note * 0.9:  # Add slight gap between notes
                        # Add some envelope to make it sound more musical
                        envelope = 1.0
                        if j < frames_per_note * 0.1:  # Attack
                            envelope = j / (frames_per_note * 0.1)
                        elif j > frames_per_note * 0.8:  # Release
                            envelope = (frames_per_note - j) / (frames_per_note * 0.2)
                        
                        wave = int(8000 * envelope * np.sin(2 * np.pi * freq * j / sample_rate))
                        audio_data[start_frame + j] = [wave, wave]
            
            # Save to temporary file
            temp_file = "temp_music.wav"
            pygame.sndarray.make_sound(audio_data).play()
            return temp_file
        except:
            return None
    
    def start_background_music(self):
        """Start playing background music."""
        if not self.music_playing and self.background_music:
            try:
                pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely
                pygame.mixer.music.set_volume(0.3)
                self.music_playing = True
            except:
                pass
    
    def stop_background_music(self):
        """Stop background music."""
        if self.music_playing:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except:
                pass
    
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
        return [0, 0, 0, 0, 0]  # Start with all zeros
    
    def save_high_scores(self):
        """Save high scores to file."""
        scores_file = "high_scores.json"
        try:
            with open(scores_file, 'w') as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def reset_high_scores(self):
        """Reset all high scores to 0."""
        self.high_scores = [0, 0, 0, 0, 0]
        self.save_high_scores()
    
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
        """Spawn a new fruit at a random location not occupied by the snake, avoiding edges."""
        while True:
            # Avoid the outer edge (1 cell border inside the playing area)
            x = random.randint(1, self.GRID_WIDTH - 2)
            y = random.randint(1, self.GRID_HEIGHT - 2)
            if (x, y) not in self.snake:
                self.fruit_pos = (x, y)
                self.fruit_type = random.choice(list(FruitType))
                break
    
    def handle_input(self, event):
        """Handle keyboard input."""
        if event.type == pygame.KEYDOWN:
            # Global quit command
            if event.key == pygame.K_q:
                return False  # Signal to quit
            
            if self.state == GameState.SPLASH:
                if event.key == pygame.K_r:
                    self.state = GameState.CONFIRM_RESET
                else:
                    self.state = GameState.PLAYING
                    self.start_background_music()
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
                elif event.key == pygame.K_r:
                    self.state = GameState.CONFIRM_RESET
            
            elif self.state == GameState.GAME_OVER:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = GameState.PLAYING
                    self.start_background_music()
                    self.last_move_time = pygame.time.get_ticks()
                elif event.key == pygame.K_h:
                    self.state = GameState.HIGH_SCORES
                elif event.key == pygame.K_r:
                    self.state = GameState.CONFIRM_RESET
            
            elif self.state == GameState.HIGH_SCORES:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = GameState.PLAYING
                    self.start_background_music()
                    self.last_move_time = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    self.state = GameState.SPLASH
                elif event.key == pygame.K_r:
                    self.state = GameState.CONFIRM_RESET
            
            elif self.state == GameState.CONFIRM_RESET:
                if event.key == pygame.K_y:
                    self.reset_high_scores()
                    self.state = GameState.SPLASH
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    self.state = GameState.SPLASH
        
        return True  # Continue running
    
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
    
    def draw_snake_segment(self, x: int, y: int, is_head: bool, segment_index: int):
        """Draw a single snake segment with improved graphics."""
        screen_x = self.PLAY_AREA_X + x * self.CELL_SIZE
        screen_y = self.PLAY_AREA_Y + y * self.CELL_SIZE
        rect = pygame.Rect(screen_x, screen_y, self.CELL_SIZE, self.CELL_SIZE)
        
        if is_head:
            # Draw snake head with eyes and direction indicator
            pygame.draw.rect(self.screen, self.GREEN, rect)
            pygame.draw.rect(self.screen, self.DARK_GREEN, rect, 2)
            
            # Draw eyes based on direction
            eye_size = 3
            if self.direction == Direction.RIGHT:
                eye1_pos = (screen_x + 14, screen_y + 6)
                eye2_pos = (screen_x + 14, screen_y + 14)
            elif self.direction == Direction.LEFT:
                eye1_pos = (screen_x + 6, screen_y + 6)
                eye2_pos = (screen_x + 6, screen_y + 14)
            elif self.direction == Direction.UP:
                eye1_pos = (screen_x + 6, screen_y + 6)
                eye2_pos = (screen_x + 14, screen_y + 6)
            else:  # DOWN
                eye1_pos = (screen_x + 6, screen_y + 14)
                eye2_pos = (screen_x + 14, screen_y + 14)
            
            pygame.draw.circle(self.screen, self.WHITE, eye1_pos, eye_size)
            pygame.draw.circle(self.screen, self.WHITE, eye2_pos, eye_size)
            pygame.draw.circle(self.screen, self.BLACK, eye1_pos, eye_size - 1)
            pygame.draw.circle(self.screen, self.BLACK, eye2_pos, eye_size - 1)
        else:
            # Draw body segment with pattern
            base_color = self.DARK_GREEN
            if segment_index % 2 == 0:
                base_color = (0, 100, 0)  # Slightly different shade for pattern
            
            pygame.draw.rect(self.screen, base_color, rect)
            pygame.draw.rect(self.screen, self.GREEN, rect, 1)
            
            # Add small scale pattern
            center_x = screen_x + self.CELL_SIZE // 2
            center_y = screen_y + self.CELL_SIZE // 2
            pygame.draw.circle(self.screen, (0, 80, 0), (center_x, center_y), 2)
    
    def draw_fruit(self, x: int, y: int, fruit_type: FruitType):
        """Draw a fruit with improved graphics based on type."""
        screen_x = self.PLAY_AREA_X + x * self.CELL_SIZE
        screen_y = self.PLAY_AREA_Y + y * self.CELL_SIZE
        center_x = screen_x + self.CELL_SIZE // 2
        center_y = screen_y + self.CELL_SIZE // 2
        
        name, primary_color, secondary_color = fruit_type.value
        
        if name == "apple":
            # Draw apple
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y + 2), 8)
            # Apple stem
            pygame.draw.rect(self.screen, secondary_color, (center_x - 1, screen_y + 2, 2, 4))
            # Apple leaf
            pygame.draw.ellipse(self.screen, secondary_color, (center_x + 2, screen_y + 2, 4, 2))
        
        elif name == "pear":
            # Draw pear shape
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y + 3), 6)
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y - 2), 4)
            # Pear stem
            pygame.draw.rect(self.screen, secondary_color, (center_x - 1, screen_y + 2, 2, 3))
        
        elif name == "banana":
            # Draw banana shape
            points = [
                (center_x - 6, center_y + 2),
                (center_x - 4, center_y - 6),
                (center_x + 2, center_y - 4),
                (center_x + 6, center_y + 4),
                (center_x + 2, center_y + 6),
                (center_x - 4, center_y + 4)
            ]
            pygame.draw.polygon(self.screen, primary_color, points)
            # Banana tip
            pygame.draw.circle(self.screen, secondary_color, (center_x - 4, center_y - 6), 2)
        
        elif name == "cherry":
            # Draw cherry (two small circles)
            pygame.draw.circle(self.screen, primary_color, (center_x - 3, center_y + 2), 5)
            pygame.draw.circle(self.screen, primary_color, (center_x + 3, center_y + 2), 5)
            # Cherry stems
            pygame.draw.line(self.screen, secondary_color, (center_x - 3, center_y - 3), (center_x - 1, center_y - 6), 2)
            pygame.draw.line(self.screen, secondary_color, (center_x + 3, center_y - 3), (center_x + 1, center_y - 6), 2)
        
        elif name == "orange":
            # Draw orange
            pygame.draw.circle(self.screen, primary_color, (center_x, center_y), 8)
            # Orange texture (small dots)
            for i in range(3):
                for j in range(3):
                    dot_x = center_x - 4 + i * 3
                    dot_y = center_y - 4 + j * 3
                    if (dot_x - center_x) ** 2 + (dot_y - center_y) ** 2 <= 36:  # Inside circle
                        pygame.draw.circle(self.screen, secondary_color, (dot_x, dot_y), 1)
    
    def draw_border(self):
        """Draw the game border."""
        # Outer border
        border_rect = pygame.Rect(0, self.UI_HEIGHT, self.WINDOW_WIDTH, self.PLAY_AREA_HEIGHT + self.BORDER_WIDTH * 2)
        pygame.draw.rect(self.screen, self.BROWN, border_rect, self.BORDER_WIDTH)
        
        # Inner playing area background
        play_rect = pygame.Rect(self.PLAY_AREA_X, self.PLAY_AREA_Y, self.PLAY_AREA_WIDTH, self.PLAY_AREA_HEIGHT)
        pygame.draw.rect(self.screen, self.BLACK, play_rect)
    
    def draw_ui(self):
        """Draw the UI area with score and length."""
        # UI background
        ui_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.UI_HEIGHT)
        pygame.draw.rect(self.screen, self.GRAY, ui_rect)
        pygame.draw.rect(self.screen, self.WHITE, ui_rect, 2)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 15))
        
        # Length
        length_text = self.font.render(f"Length: {len(self.snake)}", True, self.WHITE)
        self.screen.blit(length_text, (200, 15))
        
        # Speed indicator
        speed_percent = max(0, 100 - int((self.speed - 50) / 150 * 100))
        speed_text = self.small_font.render(f"Speed: {speed_percent}%", True, self.WHITE)
        self.screen.blit(speed_text, (400, 20))
        
        # Quit instruction
        quit_text = self.small_font.render("Press Q to quit", True, self.LIGHT_GRAY)
        self.screen.blit(quit_text, (self.WINDOW_WIDTH - 120, 20))
    
    def game_over(self):
        """Handle game over."""
        self.state = GameState.GAME_OVER
        self.update_high_scores(self.score)
        self.stop_background_music()
        
        # Play game over sound
        if self.game_over_sound:
            self.game_over_sound.set_volume(0.7)
            self.game_over_sound.play()
    
    def draw_splash_graphics(self):
        """Draw graphics for the splash screen."""
        # Draw a decorative snake
        snake_points = []
        center_x = self.WINDOW_WIDTH // 2
        for i in range(8):
            x = center_x - 100 + i * 25
            y = 100 + int(20 * math.sin(i * 0.5))
            snake_points.append((x, y))
        
        # Draw snake body
        for i, (x, y) in enumerate(snake_points):
            color = self.GREEN if i == len(snake_points) - 1 else self.DARK_GREEN
            pygame.draw.circle(self.screen, color, (x, y), 12)
            if i == len(snake_points) - 1:  # Head
                # Eyes
                pygame.draw.circle(self.screen, self.WHITE, (x + 4, y - 3), 3)
                pygame.draw.circle(self.screen, self.WHITE, (x + 4, y + 3), 3)
                pygame.draw.circle(self.screen, self.BLACK, (x + 4, y - 3), 2)
                pygame.draw.circle(self.screen, self.BLACK, (x + 4, y + 3), 2)
        
        # Draw some decorative fruits around
        fruits = [
            (100, 200, FruitType.APPLE),
            (self.WINDOW_WIDTH - 100, 180, FruitType.BANANA),
            (150, 350, FruitType.CHERRY),
            (self.WINDOW_WIDTH - 150, 320, FruitType.ORANGE),
            (center_x, 400, FruitType.PEAR)
        ]
        
        for x, y, fruit_type in fruits:
            # Convert to grid coordinates for drawing
            grid_x = (x - self.PLAY_AREA_X) // self.CELL_SIZE
            grid_y = (y - self.PLAY_AREA_Y) // self.CELL_SIZE
            # Draw directly at pixel coordinates
            screen_x = x - self.CELL_SIZE // 2
            screen_y = y - self.CELL_SIZE // 2
            center_x_fruit = screen_x + self.CELL_SIZE // 2
            center_y_fruit = screen_y + self.CELL_SIZE // 2
            
            name, primary_color, secondary_color = fruit_type.value
            
            if name == "apple":
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit, center_y_fruit + 2), 12)
                pygame.draw.rect(self.screen, secondary_color, (center_x_fruit - 1, screen_y + 2, 2, 6))
            elif name == "banana":
                points = [
                    (center_x_fruit - 8, center_y_fruit + 3),
                    (center_x_fruit - 6, center_y_fruit - 8),
                    (center_x_fruit + 3, center_y_fruit - 6),
                    (center_x_fruit + 8, center_y_fruit + 6),
                    (center_x_fruit + 3, center_y_fruit + 8),
                    (center_x_fruit - 6, center_y_fruit + 6)
                ]
                pygame.draw.polygon(self.screen, primary_color, points)
            elif name == "cherry":
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit - 4, center_y_fruit + 3), 7)
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit + 4, center_y_fruit + 3), 7)
            elif name == "orange":
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit, center_y_fruit), 12)
            elif name == "pear":
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit, center_y_fruit + 4), 8)
                pygame.draw.circle(self.screen, primary_color, (center_x_fruit, center_y_fruit - 3), 6)
    def draw_splash_screen(self):
        """Draw the splash screen."""
        self.screen.fill(self.BLACK)
        
        # Draw splash graphics
        self.draw_splash_graphics()
        
        # Title with shadow effect
        title_shadow = self.large_font.render("SNAKE GAME", True, self.DARK_GREEN)
        title_text = self.large_font.render("SNAKE GAME", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        shadow_rect = title_shadow.get_rect(center=(self.WINDOW_WIDTH // 2 + 3, 203))
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
                color = self.YELLOW if "Press" in instruction else self.WHITE
                text = self.small_font.render(instruction, True, color)
                text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_game(self):
        """Draw the game screen."""
        self.screen.fill(self.BLACK)
        
        # Draw UI and border
        self.draw_ui()
        self.draw_border()
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x, y = segment
            is_head = (i == 0)
            self.draw_snake_segment(x, y, is_head, i)
        
        # Draw fruit
        fruit_x, fruit_y = self.fruit_pos
        self.draw_fruit(fruit_x, fruit_y, self.fruit_type)
    
    def draw_game_over_screen(self):
        """Draw the game over screen."""
        self.screen.fill(self.BLACK)
        
        # Game Over title with pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        red_color = (int(255 * pulse), 0, 0)
        
        game_over_text = self.large_font.render("GAME OVER!", True, red_color)
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Check if it's a high score
        if self.score in self.high_scores[:5] and self.score > 0:
            high_score_text = self.font.render("NEW HIGH SCORE!", True, self.YELLOW)
            high_score_rect = high_score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 260))
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
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def draw_high_scores_screen(self):
        """Draw the high scores screen."""
        self.screen.fill(self.BLACK)
        
        # Title
        title_text = self.large_font.render("HIGH SCORES", True, self.YELLOW)
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # High scores with ranking colors
        colors = [self.YELLOW, self.LIGHT_GRAY, self.BROWN, self.WHITE, self.WHITE]
        y_offset = 180
        for i, score in enumerate(self.high_scores):
            color = colors[i] if i < len(colors) else self.WHITE
            score_text = self.font.render(f"{i + 1}. {score:,}", True, color)
            score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
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
            text = self.small_font.render(instruction, True, self.WHITE)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def draw_confirm_reset_screen(self):
        """Draw the confirmation screen for resetting high scores."""
        self.screen.fill(self.BLACK)
        
        # Warning title
        warning_text = self.large_font.render("RESET HIGH SCORES?", True, self.RED)
        warning_rect = warning_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        self.screen.blit(warning_text, warning_rect)
        
        # Confirmation message
        confirm_text = self.font.render("This will reset all high scores to 0", True, self.WHITE)
        confirm_rect = confirm_text.get_rect(center=(self.WINDOW_WIDTH // 2, 260))
        self.screen.blit(confirm_text, confirm_rect)
        
        # Instructions
        instructions = [
            "Press Y to confirm reset",
            "Press N or ESC to cancel"
        ]
        
        y_offset = 320
        for instruction in instructions:
            color = self.RED if "Y to confirm" in instruction else self.WHITE
            text = self.font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 40
    
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
        elif self.state == GameState.CONFIRM_RESET:
            self.draw_confirm_reset_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if not self.handle_input(event):
                        running = False
            
            self.update_game()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        self.stop_background_music()
        pygame.quit()
