"""Audio management for the Snake Game."""

from typing import Optional

import pygame

from .constants import GameConstants


class AudioManager:
    """Manages all audio for the game."""

    def __init__(self):
        """Initialize the audio manager."""
        self.initialized = False
        self.music_playing = False
        self.eat_sound: Optional[pygame.mixer.Sound] = None
        self.game_over_sound: Optional[pygame.mixer.Sound] = None
        self.move_sound: Optional[pygame.mixer.Sound] = None

        self._initialize_audio()

    def _initialize_audio(self):
        """Initialize pygame mixer and create sounds."""
        try:
            pygame.mixer.init(
                frequency=GameConstants.AUDIO_FREQUENCY,
                size=GameConstants.AUDIO_SIZE,
                channels=GameConstants.AUDIO_CHANNELS,
                buffer=GameConstants.AUDIO_BUFFER,
            )
            self._create_sound_effects()
            self._create_background_music()
            self.initialized = True
        except pygame.error:
            self.initialized = False

    def _create_sound_effects(self):
        """Create sound effects for the game."""
        try:
            self.eat_sound = pygame.mixer.Sound(buffer=self._generate_tone(440, 0.1))
            self.game_over_sound = pygame.mixer.Sound(
                buffer=self._generate_tone(220, 0.5)
            )
            self.move_sound = pygame.mixer.Sound(buffer=self._generate_tone(880, 0.05))
        except (pygame.error, ImportError):
            # Fallback if sound generation fails
            self.eat_sound = None
            self.game_over_sound = None
            self.move_sound = None

    def _create_background_music(self):
        """Create background music."""
        try:
            melody_data = self._generate_melody()
            if melody_data:
                # Save melody to a temporary buffer for pygame
                temp_sound = pygame.mixer.Sound(buffer=melody_data)
                # Note: For continuous music, we'd need to save to a file
                # For now, we'll play the generated sound in a loop
        except (pygame.error, ImportError):
            pass

    def _generate_tone(self, frequency: float, duration: float) -> bytes:
        """Generate a simple tone for sound effects.

        Args:
            frequency: Frequency of the tone in Hz
            duration: Duration of the tone in seconds

        Returns:
            Audio data as bytes
        """
        try:
            import numpy as np

            sample_rate = GameConstants.AUDIO_FREQUENCY
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2), dtype=np.int16)

            # Generate sine wave
            for i in range(frames):
                wave = int(16383 * np.sin(2 * np.pi * frequency * i / sample_rate))
                arr[i] = [wave, wave]

            return arr.tobytes()
        except ImportError:
            # Return empty bytes if numpy is not available
            return b""

    def _generate_melody(self) -> Optional[bytes]:
        """Generate a simple melodic background music.

        Returns:
            Audio data as bytes or None if generation fails
        """
        try:
            import numpy as np

            # Simple melody notes (frequencies in Hz)
            melody = [
                262,
                294,
                330,
                349,
                392,
                440,
                494,
                523,  # C major scale up
                523,
                494,
                440,
                392,
                349,
                330,
                294,
                262,  # C major scale down
                330,
                392,
                440,
                392,
                330,
                294,
                262,
                294,  # Simple melody
                330,
                349,
                392,
                349,
                330,
                294,
                262,
                262,  # Ending
            ]

            sample_rate = GameConstants.AUDIO_FREQUENCY
            note_duration = 0.5  # seconds per note
            frames_per_note = int(note_duration * sample_rate)
            total_frames = len(melody) * frames_per_note

            # Create the audio array
            audio_data = np.zeros((total_frames, 2), dtype=np.int16)

            for i, freq in enumerate(melody):
                start_frame = i * frames_per_note

                # Generate sine wave for this note
                for j in range(frames_per_note):
                    if j < frames_per_note * 0.9:  # Add slight gap between notes
                        # Add some envelope to make it sound more musical
                        envelope = 1.0
                        if j < frames_per_note * 0.1:  # Attack
                            envelope = j / (frames_per_note * 0.1)
                        elif j > frames_per_note * 0.8:  # Release
                            envelope = (frames_per_note - j) / (frames_per_note * 0.2)

                        wave = int(
                            8000 * envelope * np.sin(2 * np.pi * freq * j / sample_rate)
                        )
                        audio_data[start_frame + j] = [wave, wave]

            return audio_data.tobytes()
        except ImportError:
            return None

    def play_eat_sound(self, urgency_factor: float = 1.0):
        """Play the fruit eating sound.

        Args:
            urgency_factor: Factor to modify pitch for urgency (1.0 = normal)
        """
        if not self.initialized or not self.eat_sound:
            return

        try:
            # Create a higher pitched sound for urgency
            if urgency_factor > 1.0:
                urgent_sound = pygame.mixer.Sound(
                    buffer=self._generate_tone(440 * urgency_factor, 0.15)
                )
                urgent_sound.set_volume(0.5)
                urgent_sound.play()
            else:
                self.eat_sound.set_volume(0.5)
                self.eat_sound.play()
        except pygame.error:
            pass

    def play_move_sound(self, urgency_factor: float = 1.0):
        """Play the movement sound.

        Args:
            urgency_factor: Factor to modify pitch for urgency (1.0 = normal)
        """
        if not self.initialized or not self.move_sound:
            return

        try:
            if urgency_factor > 1.0:
                urgent_sound = pygame.mixer.Sound(
                    buffer=self._generate_tone(880 * urgency_factor, 0.03)
                )
                urgent_sound.set_volume(0.3)
                urgent_sound.play()
        except pygame.error:
            pass

    def play_game_over_sound(self):
        """Play the game over sound."""
        if not self.initialized or not self.game_over_sound:
            return

        try:
            self.game_over_sound.set_volume(0.7)
            self.game_over_sound.play()
        except pygame.error:
            pass

    def start_background_music(self):
        """Start playing background music."""
        if not self.initialized or self.music_playing:
            return

        try:
            # For now, we'll create a simple looping tone
            # In a full implementation, you'd load a music file
            melody_sound = pygame.mixer.Sound(buffer=self._generate_melody() or b"")
            if melody_sound:
                # Play the melody sound in a loop (simplified approach)
                pygame.mixer.Channel(0).play(melody_sound, loops=-1)
                pygame.mixer.Channel(0).set_volume(0.3)
                self.music_playing = True
        except (pygame.error, TypeError):
            pass

    def stop_background_music(self):
        """Stop background music."""
        if not self.initialized or not self.music_playing:
            return

        try:
            pygame.mixer.Channel(0).stop()
            self.music_playing = False
        except pygame.error:
            pass

    def cleanup(self):
        """Clean up audio resources."""
        if self.initialized:
            self.stop_background_music()
            pygame.mixer.quit()
