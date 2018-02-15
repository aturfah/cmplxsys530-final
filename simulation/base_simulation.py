"""Class for simulation that everything inherits from."""

from ladder.random_ladder import RandomLadder
from ladder.weighted_ladder import WeightedLadder
from log_manager.log_writer import LogWriter

LADDER_CHOICES = [
    WeightedLadder,
    RandomLadder
]

class BaseSimulation():
    """Base Simulation class."""

    def __init__(self, **kwargs):
        self.num_players = kwargs["num_players"]
        self.num_runs = kwargs["num_runs"]
        self.ladder_choice = kwargs["ladder_choice"]
        self.game = kwargs["game"]
        self.ladder = LADDER_CHOICES[self.ladder_choice](self.game)

        self.prefix = kwargs.get("prefix", "")

    def init_player_log_writer(self):
        """Initialize player data LogWriter."""
        header = []
        header.append("player1.type")
        header.append("player1.elo")
        header.append("player2.type")
        header.append("player2.elo")
        header.append("outcome")

        log_prefix = "{}Players".format(self.prefix)

        self.log_writer = LogWriter(header, prefix=log_prefix)
