"""Engine for Best N/M RPS."""

import numpy as np

class MTRPSEngine:
    """Multiturn RPS Engine class."""
    def __init__(self, num_games=3):
        """Initialize empty game_state"""
        self.num_games = num_games

        self.reset_game_state()


    def reset_game_state(self):
        self.game_state = np.zeros(self.num_games, dtype=bool)


