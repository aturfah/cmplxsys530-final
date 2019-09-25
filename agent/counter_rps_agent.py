"""Special RPS Agent that counters opponent."""

import logging
import typing

from agent.rps_agent import RPSAgent


class CounterRPSAgent(RPSAgent):
    """
    Class for Counter RPS Agent.

    Strategy is as follows:
        Turn1: Play strategy defined by strategy_in
        Turn2->n: Play what would beat opponent.
    """

    def __init__(self, id_in: typing.Any = None, strategy_in: typing.Union[str, list] = "uniform"):
        """Init method."""
        super().__init__(id_in=id_in, strategy_in=strategy_in)
        self.reset_state()
        self.type = "counter"
        self.last_move = None

    def reset_state(self):
        """Set the last_move to None."""
        logging.info("CounterRPSAgent:reset_state:%s", self.id)
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
        logging.info("CounterRPSAgent:make_move:%s", self.id)
        if self.last_move is None:
            return super().make_move()

        chosen_move = (self.last_move + 1) % 3
        logging.info("CounterRPSAgent:make_move:Last Move %s", self.last_move)
        logging.info("CounterRPSAgent:make_move:Chosen Move %s", chosen_move)
        return chosen_move
