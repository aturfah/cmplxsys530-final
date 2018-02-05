""" Agent class for Rock/Paper/Scissors """
from agent.base_agent import Base_Agent
from numpy.random import uniform

class RPS_Agent(Base_Agent):
    def __init__(self, strategy = [1/3, 1/3, 1/3]):
        """ 
        Create a Rock/Paper/Scissors player who plays Rock, Paper, or Scissors
        according to probabilities in strategy.

        :param strategy: Vector of probabilities to play any of Rock, Paper, Scissors respectively
        """
        if len(strategy) is not 3:
            raise ValueError('Strategy vector must be of length 3')
        if not(abs(sum(strategy) - 1) < 0.0000000000000000000001):
            # Not arbitrarily close to 1
            # TODO: Fix this its nasty
            raise ValueError('Strategy probabilities must sum to 1')

        self.strategy = strategy
        super().__init__(self)

    def make_move(self):
        num = uniform()
        for i in range(3):
            if num < sum(self.strategy[:i+1]):
                return i
        
        raise RuntimeError('Something went wrong with strategy selection')