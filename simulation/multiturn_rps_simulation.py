"""Simulation class for MultiTurn RPS Simulation."""

from math import ceil

from agent.rps_agent import RPSAgent
from agent.counter_rps_agent import CounterRPSAgent

from battle_engine.multiturn_rps import MTRPSEngine

from log_manager.log_writer import LogWriter
from stats.calc import calculate_avg_elo

from simulation.rps_simulation import BaseSimulation


class MTRPSSimulation(BaseSimulation):
    """Simulation for a multi-turn RPS Simulation."""

    def __init__(self, **kwargs):
        """Init method."""
        mtrps_kwargs = kwargs
        mtrps_kwargs["game"] = MTRPSEngine()
        mtrps_kwargs["prefix"] = "MTRPS"
        super().__init__(mtrps_kwargs)

        self.proportions = [0.3, 0.3, 0.3, 0, 0.1]
        self.data_delay = kwargs["data_delay"]


    def add_agents(self):
        """Add agents in specified proportions to the ladder."""
        num_rock = ceil(float(self.proportions[0])*self.num_players)
        num_paper = ceil(float(self.proportions[1])*self.num_players)
        num_scissors = ceil(float(self.proportions[2])*self.num_players)
        num_mixed = ceil(float(self.proportions[3])*self.num_players)
        num_counter = ceil(float(self.proportions[4])*self.num_players)

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

        for counter_ind in range(num_counter):
            agent_id = 'counter_{}'.format(counter_ind)
            player = CounterRPSAgent(id_in=agent_id)
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
        if self.proportions[4] != 0:
            header.append("counter")

        self.type_log_writer = LogWriter(header, prefix="MTRPSTypes")

    def run(self):
        """Run Rock/Paper/Scissors simulation."""
        for game_ind in range(self.num_runs):
            outcome, player1, player2 = self.ladder.run_game()

            self.write_player_log(outcome, player1, player2)

            if game_ind % self.data_delay == 0:
                # Calculate the average ranking statistics
                # every <data_delay> iterations
                self.type_log_writer.write_line(calculate_avg_elo(self.ladder))
