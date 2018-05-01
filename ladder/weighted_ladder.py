"""Methods for matching players together by elo ranking."""
from ladder.base_ladder import BaseLadder


class WeightedLadder(BaseLadder):
    """Ladder that matches players by Elo ranking."""

    def __init__(self, game=None, K_in=32):
        """
        Initialize a ladder for a specific game.

        Args:
            game (battle_engine): Game to be played on this ladder.
            K_in (int): K value to be used for calculating elo changes
                on this ladder.

        """
        super().__init__(game=game, K_in=K_in)

    def match_func(self, player1, player2_pair):
        """
        Calculate the match score for two players.

        Players with similar elo rankings should be matched together.
        In addition, players who have been waiting for a long time should
        get to play sooner.

        Functional form is <Turns_waiting>/abs(<Difference in Elo scores>)

        Args:
            player1 (BaseAgent): The player who is being matched.
            player2_pair (tuple): The candidate player & turns waiting pair for a match.

        Returns:
            The score for a match; in this case a the function defined above.

        """
        elo_factor = 1/max(abs(player1.elo - player2_pair[0].elo), 1)
        turn_factor = max((self.num_turns - player2_pair[1]), 1)

        return elo_factor*turn_factor
