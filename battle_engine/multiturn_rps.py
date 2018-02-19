"""Engine for Best N/M RPS."""

import numpy as np

class MTRPSEngine:
    """Multiturn RPS Engine class."""
    def __init__(self, num_games=3):
        """
        Initialize empty game_state.
        
        :param num_games: int
            Number of games to play.
        """
        if num_games % 2 == 0:
            raise AttributeError("num_games must be odd.")

        self.num_games = num_games
        self.reset_game_state()


    def reset_game_state(self):
        self.game_state = np.zeros(self.num_games, dtype=bool)


