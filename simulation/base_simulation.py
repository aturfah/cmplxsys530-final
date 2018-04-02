"""Class for simulation that everything inherits from."""

from time import time

from ladder.random_ladder import RandomLadder
from ladder.weighted_ladder import WeightedLadder

from log_manager.log_writer import LogWriter

LADDER_CHOICES = [
    WeightedLadder,
    RandomLadder
]


class BaseSimulation():
    """Base Simulation class."""

    def __init__(self, kwargs):
        """
        Init method.

        :param num_games: int
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
        self.num_games = kwargs["num_games"]
        self.game = kwargs["game"]
        self.ladder_choice = kwargs["ladder_choice"]
        self.ladder = LADDER_CHOICES[self.ladder_choice](self.game)

        self.prefix = kwargs.get("prefix", "")
        self.init_player_log_writer()

    def write_player_log(self, outcome, player1, player2):
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

    def print_progress_bar(self, iter_num, start_time):
        """
        Call in a loop to create terminal progress bar.

        Code borrowed/modified from:
        https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
        """
        iteration = iter_num + 1
        total = self.num_games
        prefix = "Progress: "
        suffix = "Complete"
        length = 50
        fill = '█'
        percent = ("{0:." + str(1) + "f}").format(100 *
                                                  (iteration / float(total)))
        exact_progress = "{}/{}".format(iteration, total)
        filled_length = int(length * iteration // total)
        time_remaining = str(int((time() - start_time)*total/(iter_num+0.1)))
        bars = fill * filled_length + '-' * (length - filled_length)

        print('\r%s |%s| (%s) %s%% %s | ETA: %ss' %
              (prefix, bars, exact_progress, percent, suffix, time_remaining), end='\r')

        # Print New Line on Complete
        if iteration == total:
            print("\r\n\r\n")

    def run(self):
        """Run this simulation."""
        raise NotImplementedError("Implement in inherited class")
