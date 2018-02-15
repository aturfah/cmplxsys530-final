"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from simulation.base_simulation import BaseSimulation
from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from stats.calc import calculate_avg_elo
# from stats.plot import plot_group_ratings
from log_manager.log_writer import LogWriter


class RPSSimulation(BaseSimulation):
    """Class for running an RPS Simulation."""

    def __init__(self, **kwargs):
        rps_kwargs = kwargs
        rps_kwargs["game"] = RPSEngine()
        rps_kwargs["prefix"] = "RPS"
        super().__init__(rps_kwargs)

        self.proportions = kwargs["proportions"]
        self.data_delay = kwargs["data_delay"]

        self.add_agents()
        self.init_type_log_writer()

    def add_agents(self):
        """Add agents in specified proportions to ladder."""
        num_rock = ceil(float(self.proportions[0])*self.num_players)
        num_paper = ceil(float(self.proportions[1])*self.num_players)
        num_scissors = ceil(float(self.proportions[2])*self.num_players)
        num_mixed = ceil(float(self.proportions[3])*self.num_players)

        for rock_ind in range(num_rock):
            agent_id = 'rock_{}'.format(rock_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='rock')
            self.ladder.add_player(player)

        for paper_ind in range(num_paper):
            agent_id = 'paper_{}'.format(paper_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='paper')
            self.ladder.add_player(player)

        for sciss_ind in range(num_scissors):
            agent_id = 'scissors_{}'.format(sciss_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='scissors')
            self.ladder.add_player(player)

        for mixed_ind in range(num_mixed):
            agent_id = 'mixed_{}'.format(mixed_ind)
            player = RPSAgent(id_in=agent_id)
            self.ladder.add_player(player)

    def init_type_log_writer(self):
        """Initialize Type Average Elo LogWriter."""
        header = []
        if self.proportions[0] != 0:
            header.append("rock")
        if self.proportions[1] != 0:
            header.append("paper")
        if self.proportions[2] != 0:
            header.append("scissors")
        if self.proportions[3] != 0:
            header.append("uniform")

        self.type_log_writer = LogWriter(header, prefix="RPSTypes")

    def run(self):
        """Run Rock/Paper/Scissors simulation"""
        for game_ind in range(self.num_runs):
            outcome, player1, player2 = self.ladder.run_game()

            self.write_player_log(outcome, player1, player2)

            if game_ind % self.data_delay == 0:
                # Calculate the average ranking statistics
                # every <data_delay> iterations
                self.type_log_writer.write_line(calculate_avg_elo(self.ladder))
