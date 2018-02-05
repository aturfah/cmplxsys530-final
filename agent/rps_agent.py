""" Agent class for Rock/Paper/Scissors """
from agent.base_agent import Base_Agent

class RPS_Agent(Base_Agent):
    def __init__(self, strategy = [1/3, 1/3, 1/3]):
        """ 
        Create a Rock/Paper/Scissors player who plays Rock, Paper, or Scissors
        according to probabilities in strategy.

        :param strategy: Vector of probabilities to play any of Rock, Paper, Scissors respectively
        """
        if length(strategy) is not 3:
            raise ValueError('Strategy vector must be of length 3')
        if sum(strategy) is not 1:
            raise ValueError('Strategy probabilities must sum to 1')

        self.strategy = strategy
        super()__init__(self)
