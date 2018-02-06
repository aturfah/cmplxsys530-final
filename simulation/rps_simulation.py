"""Script to run a ladder simulation for Rock Paper Scissors."""

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent
from ladder.ladder import Ladder
from stats.calc import calculate_avg_elo
from stats.plot import plot_group_ratings


def run(num_runs, num_players, proportions,
        suppress_print, suppress_graph, data_delay):
    """Run a Rock/Paper/Scissors simulation."""
    game = RPSEngine()
    lad = Ladder()
    ratings = {}

    add_agents(lad, num_players, proportions)

    for game_ind in range(num_runs):
        lad.run_game(game)
        if game_ind % data_delay == 0:
            # Calculate the statistics every 10 values
            current_stats = calculate_avg_elo(lad)
            for group in current_stats:
                if group not in ratings:
                    ratings[group] = []
                ratings[group].append(current_stats[group])

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
