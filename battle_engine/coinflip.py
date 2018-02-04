""" Coin Flip Engine, random chance of winning """
from numpy.random import uniform


class CoinFlipEngine:
    def __init__(self, prob_win=0.5):
        """
        Initialize a random Coin Flip Engine, winner decided by a coin flip

        :param player1: Agent that will participate in the game
        :param player2: The other agent that will participate in the game
        :param prob_win: Probability player1 wins
        """
        if prob_win > 1 or prob_win < 0:
            raise AttributeError("prob_win must be between 0 and 1")

        self.prob_win = prob_win

    def run(self, player1, player2):
        """ Run the game, in this case draw from U(0,1)"""
        draw = uniform()

        if draw < self.prob_win:
            # Player1 wins
            return 1
        else:
            # Player2 wins
            return 0
