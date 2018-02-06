"""Engine implementation for Rock, Paper, Scissors."""
from numpy.random import uniform


class RPSEngine:
    """Engine to run a game of rock, paper, scissors."""

    def __init__(self, bias=0.5):
        """
        Init method for this class.

        :param bias: How biased this class is in tiebreaking.
        """
        self.bias = bias

    def run(self, player1, player2):
        """Run a game of Rock, Paper, Scissors."""
        p1_move = player1.make_move()
        p2_move = player2.make_move()

        if p1_move == p2_move:
            # Same move, call it with a coinflip
            return uniform() > self.bias
        elif (p1_move - p2_move) == 1 or (p1_move - p2_move) == -2:
            # Player1 wins (Paper vs Rock or
            #   Scissors vs Paper or Rock vs Scissors)
            return 1

        # Player2 wins
        return 0
