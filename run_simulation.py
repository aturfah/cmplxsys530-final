""" Script to run a ladder simulation """
import click

from simulation import cfe_simulation
from simulation import rps_simulation

@click.command()
@click.option('--num_runs', default=5000, help='Number of games to simulate')
@click.option('--num_players', default=10, help='Number of agents')
@click.option('--game_choice', default=0, help='Which game to play. Options are:\n\t [0] Coin Flip\n\t [1] Rock Paper Scissors')
def run(num_runs, num_players, game_choice):
    if game_choice == 0:
        cfe_simulation.run(num_runs, num_players)
    elif game_choice == 1:
        rps_simulation.run(num_runs, num_players)

if __name__ == "__main__":
    run()
