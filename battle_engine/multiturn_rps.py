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
        self.game_state = {}
        self.game_state[0] = 0
        self.game_state[1] = 0
        self.game_state[2] = 0

    def run(self, player1, player2):
        """Run a set of games."""
        self.reset_game_state()
        outcome = None
        for index in range(self.num_games):
            p1_move = player1.make_move()
            p2_move = player2.make_move()

            if p1_move == p2_move:
                # Draw
                self.game_state[0] += 1
            elif (p1_move - p2_move) == 1 or (p1_move - p2_move) == -2:
                # player1 wins (Paper vs Rock or
                #   Scissors vs Paper or Rock vs Scissors)
                self.game_state[1] += 1
            else:
                # player2 wins
                self.game_state[2] += 1

            outcome = self.win_condition_met()
            if not outcome["draw"]:
                print("Player{} won in {} turns".format(
                    outcome["winner"], index))
                break

        if not outcome["draw"]:
            return outcome["winner"]

        return int(uniform() < 0.5)

    def win_condition_met(self):
        """
        Assess whether or not condition for winning met and return winner.

        If number of games necessary for victory met, return the winner.
        """
        p1_wins = self.game_state[1]
        p2_wins = self.game_state[2]
        wins_needed = int(self.num_games/2)+1

        # Initialize results
        result = {}
        result["draw"] = True
        result["winner"] = None

        if p1_wins >= wins_needed:
            result["draw"] = False
            result["winner"] = 1
        elif p2_wins >= wins_needed:
            result["draw"] = False
            result["winner"] = 2

        return result
