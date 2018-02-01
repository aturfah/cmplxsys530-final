""" Coin Flip Engine, random chance of winning """
from ladder.elo import elo
from numpy.random import uniform

class CoinFlipEngine:
    def __init__(self, player1, player2, prob_win = 0.5):
        """
        Initialize a random Coin Flip Engine, winner decided by a coin flip

        :param player1: Agent that will participate in the game
        :param player2: The other agent that will participate in the game
        :param prob_win: Probability player1 wins
        """
        if prob_win > 1 or prob_win < 0:
            raise AttributeError("prob_win must be between 0 and 1")

        self.p1 = player1
        self.p2 = player2
        self.prob_win = prob_win

    def results(winner, loser):
        """ Update values for winner and loser """
        new_winner_elo = elo(winner, loser, 1)
        new_loser_elo = elo(winner, loser, 0)
        winner.elo = new_winner_elo
        winner.num_wins += 1
        loser.elo = new_loser_elo
        loser.num_losses += 1

    def run(self):
        """ Run the game, in this case draw from U(0,1)"""
        draw = uniform()

        if draw < self.prob_win:
            # Player1 wins
            results(self.p1, self.p2)
        else:
            # Player2 wins
            results(self.p2, self.p1)