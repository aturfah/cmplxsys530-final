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
        """
        Init method.

        :param num_runs: int
            Total number of games to simulate
        :param num_players: int
            Approximate number of players to have on the ladder
        :param game: GameEngine
            Game to play in this simulation
        :param ladder_choice: int
            Whether to use WeightedLadder (0) or RandomLadder (1)
            for ladder matching.
        :param ladder: BaseLadder
            Ladder to run this simulation with.
        """
        self.num_players = kwargs["num_players"]
        self.num_runs = kwargs["num_runs"]
        self.game = kwargs["game"]
        self.ladder_choice = kwargs["ladder_choice"]
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

    def run(self, **kwargs):
        """Run this simulation."""
        raise NotImplementedError("Implement in inherited class")
