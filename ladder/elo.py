"""Functions to compute new elo values for a player."""
from math import floor


def expected(player1, player2):
    """
    Calculate expected score of player1 vs player2 given elo rankings.

    Args:
        player1 (BaseAgent): Agent for whom the score is being calculated.
        player2 (BaseAgent): Agent against whom player1 played.

    Returns:
        The expected score of the matchup.

    """
    return 1 / (1 + 10 ** ((player2.elo - player1.elo) / 400))


def elo(player1, player2, outcome, k=32):
    """
    Calculate new elo score given outcome of match.

    Args:
        player1 (BaseAgent): Agent for whom the score is being calculated.
        player2 (BaseAgent): Agent against whom player1 played.
        outcome (int): Results of the game between the players. Can be win (1)
            or loss(0), there are no draws.
        k (int): K value used in the calculation.

    Returns:
        The new elo score for player1

    """
    exp = expected(player1, player2)
    new_elo = floor(player1.elo + k * (outcome - exp))
    return max(new_elo, 1000)
