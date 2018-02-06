""" Script to run a ladder simulation """
import click

from simulation import cfe_simulation
from simulation import rps_simulation


@click.command()
@click.option('-nr', '--num_runs', default=5000, help='Number of games to simulate')
@click.option('-np', '--num_players', default=10, help='Number of agents')
@click.option('-g', '--game_choice', default=0, help="""Which game to play. Options are:\n\t [0] Coin Flip\n\t [1] Balanced Rock Paper Scissors\n\t [2] Skewed RPS""")
@click.option('-p', '--proportions', nargs=4, default=(0.25, 0.25, 0.25, 0.25), help="Proportions for skewed RPS tournament")
@click.option('-sp', '--suppress_print', default=False, is_flag=True, help="Suppress print output")
@click.option('-sg', '--suppress_graph', default=False, is_flag=True, help="Suppress graphical output")
@click.option('-dd', '--data_delay', default=10, help='Number of iterations between gathering data')
def run(num_runs, num_players, game_choice, proportions, suppress_print, suppress_graph, data_delay):
    if game_choice == 0:
        cfe_simulation.run(num_runs, num_players, suppress_print)
    elif game_choice == 1:
        rps_simulation.run(num_runs=num_runs,
                           num_players=num_players,
                           proportions = (0.25, 0.25, 0.25, 0.25),
                           data_delay=data_delay,
                           suppress_print=suppress_print,
                           suppress_graph=suppress_graph)
    elif game_choice == 2:
        rps_simulation.run(num_runs=num_runs,
                           num_players=num_players,
                           proportions=proportions,
                           data_delay=data_delay,
                           suppress_print=suppress_print,
                           suppress_graph=suppress_graph)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
