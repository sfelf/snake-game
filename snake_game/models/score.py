"""Score management for the Snake Game."""

import json
import os
from typing import List


class ScoreManager:
    """Manages game scoring and high scores."""
    
    def __init__(self, scores_file: str = "high_scores.json", max_scores: int = 5):
        """Initialize the score manager.
        
        Args:
            scores_file: File to store high scores
            max_scores: Maximum number of high scores to keep
        """
        self.scores_file = scores_file
        self.max_scores = max_scores
        self.current_score = 0
        self.high_scores = self._load_high_scores()
    
    def _load_high_scores(self) -> List[int]:
        """Load high scores from file.
        
        Returns:
            List of high scores, defaults to all zeros
        """
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    scores = json.load(f)
                    return sorted(scores, reverse=True)[:self.max_scores]
        except (json.JSONDecodeError, IOError):
            pass
        
        return [0] * self.max_scores
    
    def _save_high_scores(self):
        """Save high scores to file."""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_scores, f)
        except IOError:
            pass  # Fail silently if we can't save
    
    def add_points(self, points: int):
        """Add points to the current score.
        
        Args:
            points: Points to add
        """
        self.current_score += points
    
    def reset_current_score(self):
        """Reset the current score to zero."""
        self.current_score = 0
    
    def update_high_scores(self, score: int = None) -> bool:
        """Update high scores with a new score.
        
        Args:
            score: Score to add (uses current_score if None)
            
        Returns:
            True if it's a new high score
        """
        if score is None:
            score = self.current_score
        
        if score > 0:  # Only add non-zero scores
            self.high_scores.append(score)
            self.high_scores = sorted(self.high_scores, reverse=True)[:self.max_scores]
            self._save_high_scores()
            return score in self.high_scores[:self.max_scores]
        
        return False
    
    def reset_high_scores(self):
        """Reset all high scores to zero."""
        self.high_scores = [0] * self.max_scores
        self._save_high_scores()
    
    def is_high_score(self, score: int = None) -> bool:
        """Check if a score would be a high score.
        
        Args:
            score: Score to check (uses current_score if None)
            
        Returns:
            True if it would be a high score
        """
        if score is None:
            score = self.current_score
        
        return score > min(self.high_scores) or 0 in self.high_scores
    
    def get_high_scores(self) -> List[int]:
        """Get a copy of the high scores list.
        
        Returns:
            List of high scores
        """
        return self.high_scores.copy()
    
    @property
    def score(self) -> int:
        """Get the current score."""
        return self.current_score
