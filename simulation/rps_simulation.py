"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from ladder.weighted_ladder import WeightedLadder
from ladder.random_ladder import RandomLadder
from stats.calc import calculate_avg_elo
# from stats.plot import plot_group_ratings
from log_manager.log_writer import LogWriter

from simulation.base_simulation import BaseSimulation


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


LADDER_CHOICES = [
    WeightedLadder,
    RandomLadder
]


def run(**kwargs):
    """
    Run a Rock/Paper/Scissors simulation.

    :param num_runs: int
        Total number of games to simulate
    :param num_players: int
        Approximate number of players to have on the ladder
    :param proportions: list
        List proportions of Rock, Paper, Scissors, Uniform players
        to have on the ladder.
    :param data_delay: int
        How often to record the elo rankings of the players for graphing
    """
    num_runs = kwargs["num_runs"]
    num_players = kwargs["num_players"]
    proportions = kwargs["proportions"]
    data_delay = kwargs["data_delay"]
    ladder_choice = kwargs["ladder_choice"]

    game = RPSEngine()
    lad = LADDER_CHOICES[ladder_choice](game)
    player_log_writer = init_player_log_writer()
    type_log_writer = init_type_log_writer(proportions)

    add_agents(lad, num_players, proportions)

    for game_ind in range(num_runs):
        outcome, player1, player2 = lad.run_game()

        datum = {
            "player1.type": player1.type,
            "player1.elo": player1.elo,
            "player2.type": player2.type,
            "player2.elo": player2.elo,
            "outcome": outcome
        }
        player_log_writer.write_line(datum)

        if game_ind % data_delay == 0:
            # Calculate the average ranking statistics
            # every <data_delay> iterations
            type_log_writer.write_line(calculate_avg_elo(lad))


def add_agents(lad, num_players, proportions):
    """Add agents in specified proportions to ladder."""
    num_rock = ceil(float(proportions[0])*num_players)
    num_paper = ceil(float(proportions[1])*num_players)
    num_scissors = ceil(float(proportions[2])*num_players)
    num_mixed = ceil(float(proportions[3])*num_players)

    for rock_ind in range(num_rock):
        agent_id = 'rock_{}'.format(rock_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='rock')
        lad.add_player(player)

    for paper_ind in range(num_paper):
        agent_id = 'paper_{}'.format(paper_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='paper')
        lad.add_player(player)

    for sciss_ind in range(num_scissors):
        agent_id = 'scissors_{}'.format(sciss_ind)
        player = RPSAgent(id_in=agent_id, strategy_in='scissors')
        lad.add_player(player)

    for mixed_ind in range(num_mixed):
        agent_id = 'mixed_{}'.format(mixed_ind)
        player = RPSAgent(id_in=agent_id)
        lad.add_player(player)


def init_player_log_writer():
    """Initialize player data LogWriter."""
    header = []
    header.append("player1.type")
    header.append("player1.elo")
    header.append("player2.type")
    header.append("player2.elo")
    header.append("outcome")

    log_writer = LogWriter(header, prefix="RPSPlayers")
    return log_writer


def init_type_log_writer(proportions):
    """Initialize Type Average Elo LogWriter."""
    header = []
    if proportions[0] != 0:
        header.append("rock")
    if proportions[1] != 0:
        header.append("paper")
    if proportions[2] != 0:
        header.append("scissors")
    if proportions[3] != 0:
        header.append("uniform")

    log_writer = LogWriter(header, prefix="RPSTypes")
    return log_writer
