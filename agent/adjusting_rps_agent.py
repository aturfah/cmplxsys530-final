"""RPS Agent who updates based on all games played."""

from copy import deepcopy

from agent.rps_agent import RPSAgent


class AdjustingRPSAgent(RPSAgent):
    """
    Class for the AdjustingRPSAgent

    Updates strategy based on all games played.
    """

    def __init__(self, id_in=None, strategy_in="uniform", weight=1):
        """Initialize this Agent."""
        super().__init__(id_in=id_in, strategy_in=strategy_in)
        self.type = "PopnAdjust"
        self.original_strategy = deepcopy(self.strategy)
        self.counts = [val * weight for val in self.strategy]
        self.weight = weight

    def reset_state(self):
        """Reset state once game is finished."""
        self.strategy = deepcopy(self.original_strategy)
        self.counts = [int(val * self.weight) for val in self.strategy]

    def update_info(self, *args, **kwargs):
        """Update the agent's counts and strategy."""
        opp_move = kwargs.get("opp_move")
        self.counts[(opp_move + 1) % 3] += 1
        self.strategy = [val/sum(self.counts) for val in self.counts]
