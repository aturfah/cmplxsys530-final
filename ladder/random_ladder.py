"""Ladder that randomly pairs two agents."""

from random import random
from ladder.base_ladder import BaseLadder


class RandomLadder(BaseLadder):
    """Ladder that matches players randomly."""

    def __init__(self, game=None, K_in=32, selection_size=1):
        """
        Initialize a ladder for a specific game.

        Args:
            game (battle_engine): Game to be played on this ladder.
            K_in (int): K value to be used for calculating elo changes
                on this ladder.

        """
        super().__init__(game=game, K_in=K_in, selection_size=selection_size)

    def match_func(self, player1, player2_pair):
        """
        Return random value as a match weighting.

        Since players will be sorted this random value, it is
        equivalent to randomly choosing an opponent.

        Args:
            player1 (BaseAgent): The player who is being matched.
            player2_pair (tuple): The candidate player & turns waiting pair for a match.

        Returns:
            The score for a match; in this case a random number.

        """
        return random()
