"""Ladder that randomly pairs two agents."""

from numpy.random import rand
from ladder.base_ladder import BaseLadder


class RandomLadder(BaseLadder):
    """Ladder that matches players randomly."""

    def __init__(self, game=None, K_in=32):
        """
        Initialize a ladder for a specific game.

        :param game: GameEngine
            Game to be played on this ladder
        :param K_in: int
            K value to be used for calculating elo changes
            on this ladder
        """
        super().__init__(game=game, K_in=K_in)

    def match_func(self, player1, player2_pair):
        """
        Return random value as a match weighting.

        Since players will be sorted this random value, it is
        equivalent to randomly choosing an opponent.

        :param player1: BaseAgent
            The player who is being matched
        :param player2: (BaseAgent, int)
            The candidate player & turns waiting pair for a  match
        """
        return rand()
