"""Base agent class."""
from uuid import uuid4


class BaseAgent():
    """The Base Agent Class."""

    def __init__(self, id_in=None):
        """Initialize a new agent."""
        if id_in is None:
            self.id = uuid4()  # pylint: disable=C0103
        else:
            self.id = id_in  # pylint: disable=C0103

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
        print("\tW/L Ratio: {} ({})".format(
            self.win_loss_ratio(), self.total_games()))

    def make_move(self):
        """Make a move, must be overwritten by child class."""
        raise NotImplementedError
