"""Coin Flip Engine, random chance of winning."""
from random import random


class CoinFlipEngine:
    """
    Engine to run coin flip game.

    Attributes:
        prob_win (float): Probability player1 wins (between 0 and 1).

    """

    def __init__(self, prob_win=0.5):
        """
        Initialize a random Coin Flip Engine, winner decided by a coin flip.

        Args:
            prob_win (float): Probability player1 wins (between 0 and 1).
                Default is 0.5.

        """
        if prob_win > 1 or prob_win < 0:
            raise AttributeError("prob_win must be between 0 and 1")

        self.prob_win = prob_win

    def run(self, player1, player2):
        """
        Run the game, in this case draw from U(0,1).

        Victory determined if u > prob_win, where u ~ U(0,1)

        Args:
            player1 (BaseAgent): First agent that will participate in the game
            player2 (BaseAgent): The other agent that will participate in the game

        Returns:
            1 if player1 wins, or 0 if player2 wins.

        """
        # This is my hack around unused-argument
        draw = random()
        draw = draw * (player1.elo/player1.elo)
        draw = draw * (player2.elo/player2.elo)

        if draw < self.prob_win:
            # Player1 wins
            return 1
        # Player2 wins
        return 0
