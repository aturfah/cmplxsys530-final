"""Special RPS Agent that counters opponent."""

from agent.rps_agent import RPSAgent
import logging


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
        self.type = "counter"
        self.last_move = None

    def reset_state(self):
        """Reset state once game is finished."""
        self.last_move = None

    def update_info(self, *_, **kwargs):
        """Store opponent's last move."""
        last_move = kwargs.get("last_move")
        logging.info("CounterRPSAgent:update_info:%s", self.id)
        logging.info("CounterRPSAgent:update_info:Last Move %s", last_move)
        self.last_move = last_move

    def make_move(self):
        """
        Counter opponent's last move.

        On the first turn, it will play one of R, P, S with probability 1/3. On
        all subsequent turns, it will play the move that beats the opponent's last
        move.

        Returns:
            Move corresponding to Rock, Paper, or Scissors, defined by strategy above.

        """
        if self.last_move is None:
            return super().make_move()

        chosen_move = (self.last_move + 1) % 3
        logging.debug("CounterRPSAgent:make_move:Last Move %s", self.last_move)
        logging.info("CounterRPSAgent:make_move:Chosen Move %s", chosen_move)
        return chosen_move
