"""Parent class for the simulations that log data by player type."""

from time import time
from simulation.base_simulation import BaseSimulation
from stats.calc import calculate_avg_elo

class BaseLoggingSimulation(BaseSimulation):
    """Class for Simulations that log data."""

    def __init__(self, kwargs):
        """Initialize this simulation."""
        super().__init__(kwargs)
        self.type_log_writer = None
        self.data_delay = kwargs["data_delay"]

    def init_type_log_writer(self):
        """Initailize the Log Writer."""
        raise NotImplementedError("Implement initialization of log writer.")

    def run(self):
        """Run this simulation."""
        start_time = time()
        for game_ind in range(self.num_games):
            outcome, player1, player2 = self.ladder.run_game()

            self.print_progress_bar(game_ind, start_time)
            self.write_player_log(outcome, player1, player2)

            if game_ind % self.data_delay == 0:
                # Calculate the average ranking statistics
                # every <data_delay> iterations
                self.type_log_writer.write_line(calculate_avg_elo(self.ladder))
