"""
Snake Game - Main Game Controller

Copyright (c) 2025 Thomas Nelson (https://github.com/sfelf)
Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""

import pygame

from snake_game.controllers.input_handler import InputHandler
from snake_game.models import Fruit, GameState, GameStateManager, ScoreManager, Snake
from snake_game.utils import AudioManager, GameConstants
from snake_game.views import GameRenderer


class GameController:
    """Main controller that orchestrates the game."""

    def __init__(self):
        """Initialize the game controller."""
        # Initialize pygame
        pygame.init()

        # Create screen and basic pygame objects
        self.screen = pygame.display.set_mode(
            (GameConstants.WINDOW_WIDTH, GameConstants.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        # Initialize game components
        self.snake = Snake(
            GameConstants.INITIAL_SNAKE_LENGTH,
            GameConstants.GRID_WIDTH // 2,
            GameConstants.GRID_HEIGHT // 2,
        )
        self.fruit = Fruit(GameConstants.GRID_WIDTH, GameConstants.GRID_HEIGHT)
        self.state_manager = GameStateManager()
        self.score_manager = ScoreManager()
        self.renderer = GameRenderer(self.screen)
        self.input_handler = InputHandler()
        self.audio_manager = AudioManager()

        # Game timing
        self.speed = GameConstants.INITIAL_SPEED
        self.last_move_time = 0

        # Initialize game
        self._reset_game()

    def run(self) -> None:
        """Main game loop."""
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    action = self.input_handler.handle_event(
                        event, self.state_manager.current_state
                    )
                    if action == "quit":
                        running = False
                    elif action:
                        self._handle_action(action)

            # Update game logic
            self._update()

            # Render
            self._render()

            # Control frame rate
            self.clock.tick(GameConstants.TARGET_FPS)

        # Cleanup
        self.audio_manager.cleanup()
        pygame.quit()

    def _handle_action(self, action: str) -> None:
        """Handle a game action.

        Args:
            action: Action string to handle
        """
        if action.startswith("move_"):
            self._handle_movement_action(action)
        elif action in ["start_game", "restart_game"]:
            self._handle_game_start_action(action)
        elif action in ["show_splash", "show_high_scores", "show_reset_confirm"]:
            self._handle_navigation_action(action)
        elif action in ["confirm_reset", "cancel_reset"]:
            self._handle_reset_action(action)

    def _handle_movement_action(self, action: str) -> None:
        """Handle movement-related actions."""
        direction = self.input_handler.get_direction_from_action(action)
        if direction:
            self.snake.set_direction(direction)

    def _handle_game_start_action(self, action: str) -> None:
        """Handle game start actions."""
        if action == "start_game":
            self._start_game()
        elif action == "restart_game":
            self._restart_game()

    def _handle_navigation_action(self, action: str) -> None:
        """Handle navigation actions."""
        state_map = {
            "show_splash": GameState.SPLASH,
            "show_high_scores": GameState.HIGH_SCORES,
            "show_reset_confirm": GameState.CONFIRM_RESET,
        }
        self.state_manager.set_state(state_map[action])

    def _handle_reset_action(self, action: str) -> None:
        """Handle reset confirmation actions."""
        if action == "confirm_reset":
            self.score_manager.reset_high_scores()
        self.state_manager.set_state(GameState.SPLASH)

    def _start_game(self) -> None:
        """Start a new game."""
        self._reset_game()
        self.state_manager.set_state(GameState.PLAYING)
        self.audio_manager.start_background_music()
        self.last_move_time = pygame.time.get_ticks()

    def _restart_game(self) -> None:
        """Restart the game."""
        self._start_game()

    def _reset_game(self) -> None:
        """Reset the game to initial state."""
        self.snake.reset(
            GameConstants.INITIAL_SNAKE_LENGTH,
            GameConstants.GRID_WIDTH // 2,
            GameConstants.GRID_HEIGHT // 2,
        )
        self.fruit.spawn(self.snake.segments)
        self.score_manager.reset_current_score()
        self.speed = GameConstants.INITIAL_SPEED

    def _update(self) -> None:
        """Update game logic."""
        if not self.state_manager.is_state(GameState.PLAYING):
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.speed:
            self._move_snake()
            self.last_move_time = current_time

    def _move_snake(self) -> None:
        """Move the snake and handle game logic."""
        # Check fruit collision first to determine if snake should grow
        head_x, head_y = self.snake.head
        dx, dy = self.snake.next_direction.value
        next_head_pos = (head_x + dx, head_y + dy)

        will_eat_fruit = self.fruit.is_eaten_by(next_head_pos)

        # Move the snake (grow if eating fruit)
        self.snake.move(grow=will_eat_fruit)

        # Check wall collision
        if self.snake.check_wall_collision(
            GameConstants.GRID_WIDTH, GameConstants.GRID_HEIGHT
        ):
            self._game_over()
            return

        # Check self collision
        if self.snake.check_self_collision():
            self._game_over()
            return

        # Handle fruit eating
        if will_eat_fruit:
            self._eat_fruit()

        # Play move sound with urgency
        if self.snake.length > GameConstants.INITIAL_SNAKE_LENGTH:
            urgency_factor = min(self.snake.length / 20.0, 2.0)
            self.audio_manager.play_move_sound(urgency_factor)

    def _eat_fruit(self) -> None:
        """Handle fruit eating logic."""
        # Add points
        self.score_manager.add_points(GameConstants.POINTS_PER_FRUIT)

        # Increase speed
        self.speed = max(
            GameConstants.MIN_SPEED, self.speed - GameConstants.SPEED_INCREASE
        )

        # Spawn new fruit
        self.fruit.spawn(self.snake.segments)

        # Play eat sound with urgency
        urgency_factor = 1 + (self.snake.length / 30.0)
        self.audio_manager.play_eat_sound(urgency_factor)

    def _game_over(self) -> None:
        """Handle game over."""
        self.state_manager.set_state(GameState.GAME_OVER)
        self.score_manager.update_high_scores()
        self.audio_manager.stop_background_music()
        self.audio_manager.play_game_over_sound()

    def _render(self) -> None:
        """Render the current game state."""
        current_state = self.state_manager.current_state

        if current_state == GameState.SPLASH:
            self.renderer.render_splash_screen()
        elif current_state == GameState.PLAYING:
            self.renderer.render_game_screen(
                self.snake, self.fruit, self.score_manager.score, self.speed
            )
        elif current_state == GameState.GAME_OVER:
            is_high_score = self.score_manager.is_high_score()
            self.renderer.render_game_over_screen(
                self.score_manager.score, is_high_score
            )
        elif current_state == GameState.HIGH_SCORES:
            self.renderer.render_high_scores_screen(
                self.score_manager.get_high_scores()
            )
        elif current_state == GameState.CONFIRM_RESET:
            self.renderer.render_confirm_reset_screen()

        pygame.display.flip()
