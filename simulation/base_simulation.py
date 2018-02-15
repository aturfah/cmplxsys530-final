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
        :param prefix: str
            Prefix to use for these filenames.
        """
        self.num_players = kwargs["num_players"]
        self.num_runs = kwargs["num_runs"]
        self.game = kwargs["game"]
        self.ladder_choice = kwargs["ladder_choice"]
        self.ladder = LADDER_CHOICES[self.ladder_choice](self.game)

        self.prefix = kwargs.get("prefix", "")
        self.init_player_log_writer()

    def write_player_log(self, player1, player2, outcome):
        """Write the log of an individual game to a file."""
        datum = {
            "player1.type": player1.type,
            "player1.elo": player1.elo,
            "player2.type": player2.type,
            "player2.elo": player2.elo,
            "outcome": outcome
        }
        self.player_log_writer.write_line(datum)

    def init_player_log_writer(self):
        """
        Initialize player data LogWriter.
        
        This LogWriter generates a record of the two players
        who play a game (player-type and elo) and the outcome.
        """
        header = []
        header.append("player1.type")
        header.append("player1.elo")
        header.append("player2.type")
        header.append("player2.elo")
        header.append("outcome")

        log_prefix = "{}Players".format(self.prefix)

        self.player_log_writer = LogWriter(header, prefix=log_prefix)

    def run(self, **kwargs):
        """Run this simulation."""
        raise NotImplementedError("Implement in inherited class")
