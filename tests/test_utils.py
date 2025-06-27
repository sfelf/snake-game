"""Tests for utility modules."""

import pytest
from snake_game.utils import GameConstants, AudioManager


class TestGameConstants:
    """Test cases for GameConstants."""
    
    def test_grid_dimensions(self):
        """Test grid dimension constants."""
        assert GameConstants.GRID_WIDTH == 40
        assert GameConstants.GRID_HEIGHT == 30
        assert GameConstants.CELL_SIZE == 20
    
    def test_window_dimensions(self):
        """Test window dimension calculations."""
        expected_width = 40 * 20 + (2 * 2)  # grid_width * cell_size + borders
        expected_height = 30 * 20 + (2 * 2) + 60  # grid_height * cell_size + borders + ui
        
        assert GameConstants.WINDOW_WIDTH == expected_width
        assert GameConstants.WINDOW_HEIGHT == expected_height
    
    def test_play_area_dimensions(self):
        """Test play area dimension calculations."""
        assert GameConstants.PLAY_AREA_X == GameConstants.BORDER_WIDTH
        assert GameConstants.PLAY_AREA_Y == GameConstants.BORDER_WIDTH + GameConstants.UI_HEIGHT
        assert GameConstants.PLAY_AREA_WIDTH == GameConstants.GRID_WIDTH * GameConstants.CELL_SIZE
        assert GameConstants.PLAY_AREA_HEIGHT == GameConstants.GRID_HEIGHT * GameConstants.CELL_SIZE
    
    def test_game_mechanics_constants(self):
        """Test game mechanics constants."""
        assert GameConstants.INITIAL_SNAKE_LENGTH == 5
        assert GameConstants.INITIAL_SPEED == 200
        assert GameConstants.SPEED_INCREASE == 10
        assert GameConstants.MIN_SPEED == 50
        assert GameConstants.POINTS_PER_FRUIT == 4
    
    def test_color_constants(self):
        """Test color constants."""
        assert GameConstants.BLACK == (0, 0, 0)
        assert GameConstants.WHITE == (255, 255, 255)
        assert GameConstants.GREEN == (0, 255, 0)
        assert len(GameConstants.RED) == 3  # RGB tuple
        assert all(isinstance(c, int) and 0 <= c <= 255 for c in GameConstants.RED)


class TestAudioManager:
    """Test cases for AudioManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.audio_manager = AudioManager()
    
    def test_initialization(self):
        """Test audio manager initialization."""
        # Should initialize without errors
        assert hasattr(self.audio_manager, 'initialized')
        assert hasattr(self.audio_manager, 'music_playing')
    
    def test_sound_methods_dont_crash(self):
        """Test that sound methods don't crash even if audio fails."""
        # These should not raise exceptions even if audio is not available
        self.audio_manager.play_eat_sound()
        self.audio_manager.play_eat_sound(urgency_factor=2.0)
        self.audio_manager.play_move_sound()
        self.audio_manager.play_move_sound(urgency_factor=1.5)
        self.audio_manager.play_game_over_sound()
        self.audio_manager.start_background_music()
        self.audio_manager.stop_background_music()
    
    def test_cleanup(self):
        """Test audio cleanup."""
        # Should not raise exceptions
        self.audio_manager.cleanup()
    
    def test_music_state_tracking(self):
        """Test music state tracking."""
        initial_state = self.audio_manager.music_playing
        
        self.audio_manager.start_background_music()
        # State might change depending on audio availability
        
        self.audio_manager.stop_background_music()
        # Should stop music if it was playing
