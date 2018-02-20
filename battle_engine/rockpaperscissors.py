"""Engine implementation for Rock, Paper, Scissors."""
from numpy.random import uniform


class RPSEngine:
    """Engine to run a game of rock, paper, scissors."""

    def __init__(self, bias=0.5):
        """
        Init method for this class.

        :param bias: float
            How biased this class is in tiebreaking.
        """
        self.bias = bias

    def run(self, player1, player2):
        """
        Run a game of Rock, Paper, Scissors.

        Victory determined as follows:
            Rock < Paper < Scissors < Rock

        :param player1: BaseAgent
            First agent that will participate in the game
        :param player2: BaseAgent
            The other agent that will participate in the game
        """
        p1_move = player1.make_move()
        p2_move = player2.make_move()

        outcome = rps_logic(p1_move, p2_move)

        if outcome == 1:
            return 1
        elif outcome == 2:
            return 0

        # It was a draw
        return int(uniform() < self.bias)


def rps_logic(p1_move, p2_move):
    """
    Execute logic of RPS Game.

    Rock < Paper < Scissors < Rock
    """
    if p1_move == p2_move:
        # Same move, its a draw
        return 0
    elif (p1_move - p2_move) == 1 or (p1_move - p2_move) == -2:
        # Player1 wins (Paper vs Rock or
        #   Scissors vs Paper or Rock vs Scissors)
        return 1

    # Player2 wins
    return 2
