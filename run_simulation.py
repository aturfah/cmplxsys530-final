"""Script to run a ladder simulation."""
import click

from simulation.cfe_simulation import CFESimulation
from simulation.rps_simulation import RPSSimulation


@click.command()
@click.option("-nr",
              "--num_runs",
              default=5000,
              help="Number of games to simulate. Default is 5000")
@click.option("-np",
              "--num_players",
              default=10,
              help="Number of agents. Default is 10")
@click.option("-g",
              "--game_choice",
              help="Which game to play. Options are\n \
              [0] Coin Flip\n \
              [1] Balanced Population Rock Paper Scissors\n \
              [2] Skewed Population Rock Paper Scissors")
@click.option("-p",
              "--proportions",
              nargs=4,
              default=(0.25, 0.25, 0.25, 0.25),
              help="Proportions for skewed RPS tournament. Default is uniform.")
@click.option("-dd",
              "--data_delay",
              default=10,
              help="Number of iterations between gathering data. Default is 10.")
@click.option("-l",
              "--ladder",
              default=0,
              help="Which ladder matching to use. Options are \n[0] Weighted (default)\n[1] Random")
def run(**kwargs):
    """Run the simulation."""
    num_runs = kwargs.get("num_runs", None)
    num_players = kwargs.get("num_players", None)
    game_choice = kwargs.get("game_choice", None)
    if game_choice is None:
        raise RuntimeError("No Game Selected")
    game_choice = int(game_choice)
    proportions = kwargs.get("proportions", None)
    data_delay = kwargs.get("data_delay", None)
    ladder_choice = int(kwargs.get("ladder", None))

    if game_choice == 0:
        cfe_sim = CFESimulation(num_runs=num_runs,
                                num_players=num_players,
                                ladder_choice=ladder_choice)
        cfe_sim.run()
    elif game_choice == 1:
        rps_sim = RPSSimulation(num_runs=num_runs,
                                num_players=num_players,
                                proportions=(0.25, 0.25, 0.25, 0.25),
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.run()
    elif game_choice == 2:
        rps_sim = RPSSimulation(num_runs=num_runs,
                                num_players=num_players,
                                proportions=proportions,
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.run()
    else:
        raise RuntimeError("Invalid Game Choice")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
