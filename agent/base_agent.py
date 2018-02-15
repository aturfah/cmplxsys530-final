"""Base agent class."""
from uuid import uuid4


class BaseAgent():
    """The Base Agent Class."""

    def __init__(self, **kwargs):
        """Initialize a new agent.

        :param id: str
            Some identifier for this agent
        :param type: str
            "Type" for this agent, has meaning in
            agent subclasses
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

    def hello(self):
        """Test Method."""
        print("Hello from BaseAgent {}".format(self.id))

    def win_loss_ratio(self):
        """Get W/L Ratio for Agent."""
        if self.num_losses == 0:
            return None
        return self.num_wins / self.num_losses

    def total_games(self):
        """Total games agent has played."""
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
