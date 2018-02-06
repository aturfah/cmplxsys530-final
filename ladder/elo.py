"""Functions to compute new elo values for a player."""
from math import floor


def expected(player1, player2):
    """
    Calculate expected score of player1 vs player2 given elo rankings.

    :param player1: Agent for whom the score is being calculated
    :param player2: Agent against whom player1 played
    """
    return 1 / (1 + 10 ** ((player2.elo - player1.elo) / 400))


def elo(player1, player2, outcome, k=32):
    """
    Calculate new elo score given outcome of match.

    :param player1: Agent for whom the score is being calculated
    :param player2: Agent against whom player1 played
    :param outcome: Win (1) or loss(0) [there are no draws]
    :param k: The k-factor for the Elo score
    """
    exp = expected(player1, player2)
    new_elo = floor(player1.elo + k * (outcome - exp))
    return max(new_elo, 1000)
