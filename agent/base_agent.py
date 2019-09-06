"""Base agent class."""
from uuid import uuid4
import logging

class BaseAgent():
    """
    The Base Agent Class.

    Attributes:
        id (str): Some unique identifier for this agent.
        type (str): Classification for this agent.
        elo (int): Elo ranking for this agent.
        num_wins (int): Number of games won.
        num_losses (int): Number of games lost.
        in_game (bool): If player is currently in a game.

    """

    def __init__(self, **kwargs):
        """Initialize a new agent.

        Args:
            id (str): Some identifier for this agent.
                Default is random uuid4.
            type (str): "Type" for this agent, has meaning in
                identifying agent subclasses
        """
        if "id_in" not in kwargs:
            self.id = uuid4()  # pylint: disable=C0103
        else:
            self.id = kwargs["id_in"]  # pylint: disable=C0103

        if "type" not in kwargs:
            self.type = "Default"
        else:
            self.type = kwargs["type"]

        self.elo = 1000
        self.num_wins = 0
        self.num_losses = 0
        self.in_game = False

    def hello(self):
        """Test Method."""
        print("Hello from BaseAgent {}".format(self.id))

    def win_loss_ratio(self):
        """
        Get W/L Ratio for Agent.

        Returns:
            Win/Loss ratio (# Wins/# Losses).

        """
        if self.num_losses == 0:
            return None
        ratio = self.num_wins / self.num_losses
        logging.info("BaseAgent:win_loss_ratio:Wins:%s", self.num_wins)
        logging.info("BaseAgent:win_loss_ratio:Losses:%s", self.num_losses)
        logging.info("BaseAgent:win_loss_ratio:Ratio:%s", ratio)
        return ratio

    def total_games(self):
        """
        Total games agent has played.

        Returns:
            Total number of games this agent has played
                (# Wins + # Losses).

        """
        logging.info("BaseAgent:total_games:Wins:%s|Losses:%s", self.num_wins, self.num_losses)
        return self.num_wins + self.num_losses

    def print_info(self):
        """Print information about this agent."""
        print("Player: {}".format(self.id))
        print("\tElo: {}".format(self.elo))
        print("\tType: {}".format(self.type))
        print("\tW/L Ratio: {} ({})".format(
            self.win_loss_ratio(), self.total_games()))

    def make_move(self):
        """Make a move, must be overwritten by child class."""
        raise NotImplementedError
