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
        self.last_move = None