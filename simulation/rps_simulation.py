"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from ladder.ladder import Ladder
from stats.calc import calculate_avg_elo
from stats.plot import plot_group_ratings
from log_manager.log_writer import LogWriter


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
    :param suppress_print: bool
        Whether or not to print player ratings at the end of a round
    :param suppress_graph: bool
        Whether or not to graph player elo ratings over simulation
    """
    num_runs = kwargs["num_runs"]
    num_players = kwargs["num_players"]
    proportions = kwargs["proportions"]
    data_delay = kwargs["data_delay"]
    suppress_print = kwargs["suppress_print"]
    suppress_graph = kwargs["suppress_graph"]

    game = RPSEngine()
    lad = Ladder(game)
    log_writer = init_player_log_writer()
    ratings = {}

    add_agents(lad, num_players, proportions)

    for _ in range(num_runs):
        outcome, player1, player2 = lad.run_game()
        # if game_ind % data_delay == 0:
        #    # Calculate the statistics every data_delay values
        #    current_stats = calculate_avg_elo(lad)
        #    for group in current_stats:
        #        if group not in ratings:
        #            ratings[group] = []
        #        ratings[group].append(current_stats[group])
        datum = {
            "player1.type": player1.type,
            "player1.elo": player1.elo,
            "player2.type": player2.type,
            "player2.elo": player2.elo,
            "outcome": outcome
        }
        log_writer.write_line(datum)

    players = lad.get_players(sort=True)

    if not suppress_print:
        for player in players:
            player.print_info()

    if not suppress_graph:
        plot_group_ratings(ratings)


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
    """Initialize player data LogWriter"""
    header = []
    header.append("player1.type")
    header.append("player1.elo")
    header.append("player2.type")
    header.append("player2.elo")
    header.append("outcome")

    log_writer = LogWriter(header, prefix="RPSPlayers")
    return log_writer
