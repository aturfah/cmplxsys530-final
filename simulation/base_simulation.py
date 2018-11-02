"""Class for simulation that everything inherits from."""

from time import time
import json

from ladder.random_ladder import RandomLadder
from ladder.weighted_ladder import WeightedLadder

from file_manager.log_writer import LogWriter

LADDER_CHOICES = [
    WeightedLadder,
    RandomLadder
]


class BaseSimulation():
    """Base Simulation class."""

    def __init__(self, kwargs):
        """
        Init method for a simulation.

        Args:
            num_games (int): Total number of games to simulate.
            num_players (int): Approximate number of players to have on the ladder.
            game (class defined in battle_engine): Game to play in this simulation.
            ladder_choice (int): Whether to use WeightedLadder (0) or RandomLadder (1)
                for ladder matching.
            prefix (str): Prefix to use for these filenames.

        """
        self.num_players = kwargs["num_players"]
        self.num_games = kwargs["num_games"]
        self.game = kwargs["game"]
        self.ladder_choice = kwargs["ladder_choice"]
        self.ladder = LADDER_CHOICES[self.ladder_choice](self.game)

        self.prefix = kwargs.get("prefix", "")
        self.init_player_log_writer()

    def write_player_log(self, outcome, player1, player2):
        """
        Write the log of an individual game to a file.

        Args:
            outcome (int): Results of the game.
            player1 (BaseAgent): Player in this game.
            player2 (BaseAgent): Other player in this game.

        """
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

        Args:
            iter_num (int): Point in the simulation that we are at.
            start_time (time.time): time object representing start of simulation.

        """
        iteration = iter_num + 1
        prefix = "Progress: "
        length = 50
        fill = '█'
        percent = ("{0:." + str(1) + "f}").format(100 *
                                                  (iteration / float(self.num_games)))
        exact_progress = "{}/{}".format(iteration, self.num_games)
        filled_length = int(length * iteration // self.num_games)
        total_time = int(time()-start_time)
        time_remaining = (time() - start_time)/(float(iter_num)+0.1)
        time_remaining = str(int(time_remaining*(self.num_games-iter_num)))
        bars = fill * filled_length + '-' * (length - filled_length)

        print('\r%s |%s| (%s) %s%% | ETA: %ss (%ss)\t' %
              (prefix, bars, exact_progress,
               percent, time_remaining,
               total_time), end='\r')

        # Print New Line on Complete
        if iteration >= self.num_games:
            print("\r\n\r\n")

    def run(self):
        """Run this simulation."""
        raise NotImplementedError("Implement in inherited class")


def load_config(config_filename):
    """
    Load the population config for this simulation.

    Args:
        config_filename (str): Filename for the simulation's config.

    Returns:
        Dict containing data from the config file.

    """
    if not config_filename:
        return {}

    config_data = []
    with open(config_filename) as config_file:
        config_data = json.loads(config_file.read())

    if not config_data:
        raise RuntimeError("No Config Loaded: {}".format(config_filename))

    return config_data
