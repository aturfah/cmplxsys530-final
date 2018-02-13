"""Coin Flip Engine, random chance of winning."""
from numpy.random import uniform


class CoinFlipEngine:
    """Engine to run coin flip game."""

    def __init__(self, prob_win=0.5):
        """
        Initialize a random Coin Flip Engine, winner decided by a coin flip.

        :param prob_win: float, Optional
            Probability player1 wins (between 0 and 1)
        """
        if prob_win > 1 or prob_win < 0:
            raise AttributeError("prob_win must be between 0 and 1")

        self.prob_win = prob_win

    def run(self, player1, player2):
        """
        Run the game, in this case draw from U(0,1).

        :param player1: BaseAgent
            First agent that will participate in the game
        :param player2: BaseAgent
            The other agent that will participate in the game
        """
        draw = uniform()

        if draw < self.prob_win:
            # Player1 wins
            return 1
        elif draw > self.prob_win:
            # Player2 wins
            return 0

        # Its a draw, give it to whoever has higher elo
        return int(player1.elo > player2.elo)
