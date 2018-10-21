"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from simulation.base_simulation import load_config
from simulation.base_type_logging_simulation import BaseLoggingSimulation
from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from agent.counter_rps_agent import CounterRPSAgent
from file_manager.log_writer import LogWriter


class RPSSimulation(BaseLoggingSimulation):
    """Class for running an RPS Simulation."""

    def __init__(self, **kwargs):
        """
        Initialize an RPS Simulation.

        :param proportions: list
            List of proportions for Rock, Paper,
            Scissors, and Uniform players respectively
        :param data_delay: int
            Iteration gap to calculate average
            elo ranking for each strategy (R/P/S/U/C)
        """
        rps_kwargs = kwargs
        rps_kwargs["game"] = RPSEngine(kwargs["num_rounds"])
        rps_kwargs["prefix"] = "RPS"
        super().__init__(rps_kwargs)

        self.proportions = [float(val) for val in kwargs["proportions"]]
        self.type_log_writer = None
        self.data_delay = kwargs["data_delay"]
        self.config = load_config(kwargs["config"])

    def add_agents(self):
        """Add agents in specified proportions to ladder."""
        for conf in self.config:
            print(conf)
            num_agents = ceil(float(conf["proportion"]*self.num_players))
            for agent_ind in range(num_agents):
                player = None
                agent_id = "{}_{}".format(conf["agent_type"], agent_ind)
                if conf["agent_strategy"] is not None:
                    player = RPSAgent(id_in=agent_id, strategy_in=conf["agent_strategy"])
                else:
                    player = CounterRPSAgent(id_in=agent_id)

                player.type = conf["agent_type"]
                self.ladder.add_player(player)

        # num_rock = ceil(float(self.proportions[0])*self.num_players)
        # num_paper = ceil(float(self.proportions[1])*self.num_players)
        # num_scissors = ceil(float(self.proportions[2])*self.num_players)
        # num_mixed = ceil(float(self.proportions[3])*self.num_players)
        # num_counter = ceil(float(self.proportions[4])*self.num_players)

        # for rock_ind in range(num_rock):
        #     agent_id = 'rock_{}'.format(rock_ind)
        #     player = RPSAgent(id_in=agent_id, strategy_in='rock')
        #     self.ladder.add_player(player)

        # for paper_ind in range(num_paper):
        #     agent_id = 'paper_{}'.format(paper_ind)
        #     player = RPSAgent(id_in=agent_id, strategy_in='paper')
        #     self.ladder.add_player(player)

        # for sciss_ind in range(num_scissors):
        #     agent_id = 'scissors_{}'.format(sciss_ind)
        #     player = RPSAgent(id_in=agent_id, strategy_in='scissors')
        #     self.ladder.add_player(player)

        # for mixed_ind in range(num_mixed):
        #     agent_id = 'mixed_{}'.format(mixed_ind)
        #     player = RPSAgent(id_in=agent_id)
        #     self.ladder.add_player(player)

        # for counter_ind in range(num_counter):
        #     agent_id = 'counter_{}'.format(counter_ind)
        #     player = CounterRPSAgent(id_in=agent_id)
        #     self.ladder.add_player(player)

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

        self.type_log_writer = LogWriter(header, prefix="RPSTypes")
