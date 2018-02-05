""" Agent class for Rock/Paper/Scissors """
from agent.base_agent import Base_Agent
from numpy.random import uniform

strategies = {
    'rock': [1,0,0],
    'paper': [0,1,0],
    'scissors': [0,0,1],
    'uniform': [1/3, 1/3, 1/3]
}

class RPS_Agent(Base_Agent):
    def __init__(self, strategy_in = 'uniform'):
        """ 
        Create a Rock/Paper/Scissors player who plays Rock, Paper, or Scissors
        according to probabilities in strategy.

        :param strategy: Either a string corresponding to one of the strategies,
             or a vector of probabilities to play Rock, Paper, Scissors respectively
        """
        if isinstance(strategy_in, list):
            strategy = strategy_in
        elif strategy_in in strategies:
            strategy = strategies[strategy_in]
        else:
            raise ValueError('Invalid strategy')

        if len(strategy) is not 3:
            raise ValueError('Strategy vector must be of length 3')
        if any(strategy_prob < 0 for strategy_prob in strategy):
            raise ValueError('Strategy probabilities cannot be less than 0')
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