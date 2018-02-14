"""Script to run a ladder simulation."""
import click

from simulation import cfe_simulation
from simulation import rps_simulation


@click.command()
@click.option('-nr',
              '--num_runs',
              default=5000,
              help='Number of games to simulate. Default is 5000')
@click.option('-np',
              '--num_players',
              default=10,
              help='Number of agents. Default is 10')
@click.option('-g',
              '--game_choice',
              help="Which game to play. Options are\n[0] Coin Flip\n[1] Balanced Population Rock Paper Scissors\n[2] Skewed Population Rock Paper Scissors")
@click.option('-p',
              '--proportions',
              nargs=4,
              default=(0.25, 0.25, 0.25, 0.25),
              help="Proportions for skewed RPS tournament. Default is uniform.")
@click.option('-sp',
              '--suppress_print',
              default=False,
              is_flag=True,
              help="Suppress print output. Default is False")
@click.option('-sg',
              '--suppress_graph',
              default=False,
              is_flag=True,
              help="Suppress graphical output. Default is False")
@click.option('-dd',
              '--data_delay',
              default=10,
              help='Number of iterations between gathering data. Default is 10')
def run(**kwargs):
    """Run the simulation."""
    num_runs = kwargs.get('num_runs', None)
    num_players = kwargs.get('num_players', None)
    game_choice = int(kwargs.get('game_choice', None))
    proportions = kwargs.get('proportions', None)
    data_delay = kwargs.get('data_delay', None)
    suppress_print = kwargs.get('suppress_print', None)
    suppress_graph = kwargs.get('suppress_graph', None)
    
    if game_choice == 0:
        cfe_simulation.run(num_runs, num_players, suppress_print)
    elif game_choice == 1:
        rps_simulation.run(num_runs=num_runs,
                           num_players=num_players,
                           proportions=(0.25, 0.25, 0.25, 0.25),
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
    else:
        raise RuntimeError("Invalid Game Choice")

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
