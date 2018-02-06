"""Agent class for Rock/Paper/Scissors."""
from numpy.random import uniform

from agent.base_agent import BaseAgent

STRATEGIES = {
    'rock': [1, 0, 0],
    'paper': [0, 1, 0],
    'scissors': [0, 0, 1],
    'uniform': [1 / 3, 1 / 3, 1 / 3]
}


class RPSAgent(BaseAgent):
    """The agent class for Rock/Paper/Scissors."""

    def __init__(self, id_in=None, strategy_in='uniform'):
        """
        Create a Rock/Paper/Scissors player.

        The player plays Rock, Paper, or Scissors
        according to probabilities defined in strategy.

        :param strategy: Either a string corresponding to a strategy,
             or a vector of probabilities to play Rock, Paper,
             or Scissors respectively
        """
        if isinstance(strategy_in, list):
            strategy = strategy_in
        elif strategy_in in STRATEGIES:
            strategy = STRATEGIES[strategy_in]
        else:
            raise ValueError('Invalid strategy')

        if len(strategy) != 3:
            raise ValueError('Strategy vector must be of length 3')
        if any(strategy_prob < 0 for strategy_prob in strategy):
            raise ValueError('Strategy probabilities cannot be less than 0')
        if not abs(sum(strategy) - 1) < 0.0000000000000000000001:
            # Not arbitrarily close to 1
            raise ValueError('Strategy probabilities must sum to 1')

        self.strategy = strategy
        super().__init__(id_in=id_in)

    def make_move(self):
        """Play one of rock, paper, scissors defined by strategy."""
        num = uniform()
        for i in range(3):
            if num < sum(self.strategy[:i + 1]):
                return i

        raise RuntimeError('Something went wrong with strategy selection')

    def print_info(self):
        """Print the info on this player."""
        print("Player: {}".format(self.id))
        print("\tElo: {}".format(self.elo))
        print("\tStrategy: {}".format(self.strategy))
        print("\tW/L Ratio: {} ({})".format(
            self.win_loss_ratio(), self.total_games()))
