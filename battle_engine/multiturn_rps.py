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
        """Reset game state to all zeros."""
        self.game_state = np.zeros(self.num_games)

    def run(self, player1, player2):
        """Run a set of games."""
        self.reset_game_state()
        for index in range(self.num_games):
            p1_move = player1.make_move()
            p2_move = player2.make_move()

            if p1_move == p2_move:
                # Draw
                self.game_state[index] = 0
            elif (p1_move - p2_move) == 1 or (p1_move - p2_move) == -2:
                # player1 wins (Paper vs Rock or
                #   Scissors vs Paper or Rock vs Scissors)
                self.game_state[index] = 1
            else:
                # player2 wins
                self.game_state[index] = 2

        print(self.game_state)
