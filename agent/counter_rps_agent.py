"""Special RPS Agent that counters opponent."""

from agent.rps_agent import RPSAgent


class CounterRPSAgent(RPSAgent):
    """
    Class for Counter RPS Agent.

    Strategy is as follows:
        Turn1: Play random
        Turn2->n: Play what would beat opponent.
    """

    def __init__(self, id_in=None):
        """Init method."""
        super().__init__(id_in=id_in)
        self.reset_state()

    def reset_state(self):
        """Reset state once game is finished."""
        self.last_move = None

    def make_move(self):
        """Counter opponent's last move"""
        if self.last_move is None:
            super().make_move()
        return (self.last_move + 1) % 3
