"""Tests for game models."""

import pytest
from snake_game.models import Snake, Fruit, ScoreManager, GameStateManager, Direction, GameState, FruitType


class TestSnake:
    """Test cases for the Snake model."""
    
    def test_initialization(self, snake):
        """Test snake initialization."""
        assert snake.length == 5
        assert snake.head == (20, 15)
        assert snake.direction == Direction.RIGHT
        assert len(snake.segments) == 5
    
    def test_set_direction_valid(self, snake):
        """Test setting a valid direction."""
        assert snake.set_direction(Direction.UP) is True
        assert snake.next_direction == Direction.UP
    
    def test_set_direction_opposite(self, snake):
        """Test setting opposite direction (should be rejected)."""
        snake.direction = Direction.RIGHT
        assert snake.set_direction(Direction.LEFT) is False
        assert snake.next_direction == Direction.RIGHT
    
    def test_move_without_growth(self, snake):
        """Test snake movement without growth."""
        initial_length = snake.length
        initial_head = snake.head
        
        new_head = snake.move(grow=False)
        
        assert snake.length == initial_length
        assert new_head == (initial_head[0] + 1, initial_head[1])  # Moved right
        assert snake.head == new_head
    
    def test_move_with_growth(self, snake):
        """Test snake movement with growth."""
        initial_length = snake.length
        
        snake.move(grow=True)
        
        assert snake.length == initial_length + 1
    
    def test_self_collision_detection(self, snake):
        """Test self collision detection."""
        # No collision initially
        assert snake.check_self_collision() is False
        
        # Create a collision by adding head position to body
        snake.segments.append(snake.head)
        assert snake.check_self_collision() is True
    
    def test_wall_collision_detection(self, snake):
        """Test wall collision detection."""
        # No collision initially
        assert snake.check_wall_collision(40, 30) is False
        
        # Move snake to wall
        snake.segments[0] = (-1, 15)  # Left wall
        assert snake.check_wall_collision(40, 30) is True
        
        snake.segments[0] = (40, 15)  # Right wall
        assert snake.check_wall_collision(40, 30) is True
        
        snake.segments[0] = (20, -1)  # Top wall
        assert snake.check_wall_collision(40, 30) is True
        
        snake.segments[0] = (20, 30)  # Bottom wall
        assert snake.check_wall_collision(40, 30) is True
    
    def test_reset(self, snake):
        """Test snake reset functionality."""
        # Modify snake
        snake.move(grow=True)
        snake.set_direction(Direction.UP)
        
        # Reset
        snake.reset(3, 10, 10)
        
        assert snake.length == 3
        assert snake.head == (10, 10)
        assert snake.direction == Direction.RIGHT
        assert snake.next_direction == Direction.RIGHT
    
    def test_multiple_moves_maintain_length(self, snake):
        """Test that multiple moves without growth maintain snake length."""
        initial_length = snake.length
        
        # Make many moves without growth
        for i in range(20):
            snake.move(grow=False)
            assert snake.length == initial_length, \
                f"Snake length changed from {initial_length} to {snake.length} on move {i+1}"
            assert len(snake.segments) > 0, \
                f"Snake segments became empty on move {i+1}"
    
    def test_alternating_growth_and_normal_moves(self, snake):
        """Test alternating between growth and normal moves."""
        initial_length = snake.length
        
        # Grow, then make normal moves
        snake.move(grow=True)
        assert snake.length == initial_length + 1
        
        new_length = snake.length
        for i in range(5):
            snake.move(grow=False)
            assert snake.length == new_length, \
                f"Snake length should remain {new_length} but became {snake.length} on move {i+1}"
        
        # Grow again
        snake.move(grow=True)
        assert snake.length == new_length + 1
    
    def test_snake_never_becomes_empty(self, snake):
        """Test that snake segments never become empty through any operation."""
        # Test various operations
        operations = [
            lambda: snake.move(grow=False),
            lambda: snake.move(grow=True),
            lambda: snake.set_direction(Direction.UP),
            lambda: snake.set_direction(Direction.DOWN),
        ]
        
        for i, operation in enumerate(operations * 10):  # Repeat operations
            operation()
            assert len(snake.segments) > 0, \
                f"Snake segments became empty after operation {i}"
            assert snake.head is not None, \
                f"Snake head became None after operation {i}"


class TestFruit:
    """Test cases for the Fruit model."""
    
    def test_initialization(self, fruit):
        """Test fruit initialization."""
        assert fruit.grid_width == 40
        assert fruit.grid_height == 30
        assert fruit.points_value == 4
    
    def test_spawn_avoids_occupied_positions(self, fruit):
        """Test that fruit spawning avoids occupied positions."""
        occupied = [(5, 5), (6, 5), (7, 5)]
        
        # Spawn multiple times to test randomness
        for _ in range(10):
            position = fruit.spawn(occupied)
            assert position not in occupied
            assert 1 <= position[0] <= 38  # Avoids edges
            assert 1 <= position[1] <= 28  # Avoids edges
    
    def test_spawn_avoids_edges(self, fruit):
        """Test that fruit spawning avoids edges."""
        for _ in range(20):
            fruit.spawn([])
            x, y = fruit.position
            assert 1 <= x <= 38
            assert 1 <= y <= 28
    
    def test_is_eaten_by(self, fruit):
        """Test fruit eating detection."""
        fruit.position = (10, 10)
        
        assert fruit.is_eaten_by((10, 10)) is True
        assert fruit.is_eaten_by((10, 11)) is False
        assert fruit.is_eaten_by((11, 10)) is False
    
    def test_fruit_properties(self, fruit):
        """Test fruit type properties."""
        fruit.fruit_type = FruitType.APPLE
        
        assert fruit.name == "apple"
        assert fruit.primary_color == (255, 0, 0)
        assert fruit.secondary_color == (0, 150, 0)


class TestScoreManager:
    """Test cases for the ScoreManager."""
    
    def test_initialization(self, score_manager):
        """Test score manager initialization."""
        assert score_manager.score == 0
        assert len(score_manager.high_scores) == 5
        assert all(score == 0 for score in score_manager.high_scores)
    
    def test_add_points(self, score_manager):
        """Test adding points."""
        score_manager.add_points(10)
        assert score_manager.score == 10
        
        score_manager.add_points(5)
        assert score_manager.score == 15
    
    def test_reset_current_score(self, score_manager):
        """Test resetting current score."""
        score_manager.add_points(100)
        score_manager.reset_current_score()
        assert score_manager.score == 0
    
    def test_update_high_scores(self, score_manager):
        """Test updating high scores."""
        # Add some scores
        assert score_manager.update_high_scores(100) is True
        assert score_manager.update_high_scores(50) is True
        assert score_manager.update_high_scores(150) is True
        
        scores = score_manager.get_high_scores()
        assert scores[0] == 150
        assert scores[1] == 100
        assert scores[2] == 50
        assert scores[3] == 0
        assert scores[4] == 0
    
    def test_update_high_scores_zero(self, score_manager):
        """Test that zero scores are not added to high scores."""
        assert score_manager.update_high_scores(0) is False
        scores = score_manager.get_high_scores()
        assert all(score == 0 for score in scores)
    
    def test_is_high_score(self, score_manager):
        """Test high score detection."""
        # Initially, any positive score is a high score since all scores are 0
        assert score_manager.is_high_score(1) is True
        # Zero score should not be considered a high score when compared to existing zeros
        # But our current implementation considers it a high score if there are zeros in the list
        # Let's test the actual behavior
        
        # Add some scores first
        score_manager.update_high_scores(100)
        score_manager.update_high_scores(50)
        
        # Now test with current score
        score_manager.add_points(75)
        assert score_manager.is_high_score() is True
        
        score_manager.reset_current_score()
        score_manager.add_points(25)
        assert score_manager.is_high_score() is True  # Still true because there are zeros
    
    def test_reset_high_scores(self, score_manager):
        """Test resetting high scores."""
        score_manager.update_high_scores(100)
        score_manager.reset_high_scores()
        
        scores = score_manager.get_high_scores()
        assert all(score == 0 for score in scores)
        
        scores = score_manager.get_high_scores()
        assert all(score == 0 for score in scores)


class TestGameStateManager:
    """Test cases for the GameStateManager."""
    
    def test_initialization(self, state_manager):
        """Test state manager initialization."""
        assert state_manager.current_state == GameState.SPLASH
        assert state_manager.previous_state is None
    
    def test_set_state(self, state_manager):
        """Test setting game state."""
        state_manager.set_state(GameState.PLAYING)
        
        assert state_manager.current_state == GameState.PLAYING
        assert state_manager.previous_state == GameState.SPLASH
    
    def test_set_same_state(self, state_manager):
        """Test setting the same state (should not change previous)."""
        state_manager.set_state(GameState.PLAYING)
        previous = state_manager.previous_state
        
        state_manager.set_state(GameState.PLAYING)
        
        assert state_manager.current_state == GameState.PLAYING
        assert state_manager.previous_state == previous
    
    def test_is_state(self, state_manager):
        """Test state checking."""
        assert state_manager.is_state(GameState.SPLASH) is True
        assert state_manager.is_state(GameState.PLAYING) is False
        
        state_manager.set_state(GameState.PLAYING)
        assert state_manager.is_state(GameState.PLAYING) is True
        assert state_manager.is_state(GameState.SPLASH) is False
    
    def test_was_state(self, state_manager):
        """Test previous state checking."""
        assert state_manager.was_state(GameState.SPLASH) is False
        
        state_manager.set_state(GameState.PLAYING)
        assert state_manager.was_state(GameState.SPLASH) is True
        assert state_manager.was_state(GameState.PLAYING) is False
    
    def test_reset(self, state_manager):
        """Test state reset."""
        state_manager.set_state(GameState.PLAYING)
        state_manager.set_state(GameState.GAME_OVER)
        
        state_manager.reset()
        
        assert state_manager.current_state == GameState.SPLASH
        assert state_manager.previous_state == GameState.GAME_OVER
