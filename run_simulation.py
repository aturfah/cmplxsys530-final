""" Script to run a ladder simulation """
import click

from simulation import cfe_simulation
from simulation import balanced_rps_simulation
from simulation import skewed_rps_simulation

@click.command()
@click.option('--num_runs', default=5000, help='Number of games to simulate')
@click.option('--num_players', default=10, help='Number of agents')
@click.option('--game_choice', default=0, help="""Which game to play. Options are:\n\t [0] Coin Flip\n\t [1] Balanced Rock Paper Scissors\n\t [2] Skewed RPS""")
@click.option('--proportions', nargs=3, help="Proportions for skewed RPS tournament")
def run(num_runs, num_players, game_choice, proportions):   
    if game_choice == 0:
        cfe_simulation.run(num_runs, num_players)
    elif game_choice == 1:
        balanced_rps_simulation.run(num_runs, num_players)
    elif game_choice == 2:
        skewed_rps_simulation.run(num_runs, num_players, proportions)

if __name__ == "__main__":
    run()
