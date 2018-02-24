"""Script to run a ladder simulation."""
import click

from simulation.cf_simulation import CFSimulation
from simulation.rps_simulation import RPSSimulation


@click.command()
@click.option("-ng", "--num_games", default=5000)
@click.option("-nr", "--num_rounds", default=3)
@click.option("-np", "--num_players", default=10)
@click.option("-g", "--game_choice")
@click.option("-dd", "--data_delay", default=10)
@click.option("-l", "--ladder", default=0)
@click.argument("-p", "--proportions", nargs=-1)
@click.option("-f", "--file", nargs=1)
def run(**kwargs):
    """
    Run the simulation.

    Arguments are as follows:\n
    --file/-f:          Read arguments from file.
    --num_games/-ng:    Number of games to simulate.\n
                            Default is 5000\n
    --num_rounds/-nr:   Number of rounds ber game in Multi-Turn RPS.\n
                            Default is 3.\n
    --num_playeres/-np: Number of agents in the simulation.\n
                            Default is 10.\n
    --proportions/-p:   Proportions for RPS Simulations.\n
                            5 Values corresponding to RPSUC respectively.\n
    --ladder/-l:        Which ladder matching to use. Options are:\n
                            [0] Weighted (default)\n
                            [1] Random\n
    --game_choice/-g:  Choice of game to play. Options are:\n
                            [0] Coin Flip\n
                            [1] Balanced Population RPS\n
                            [2] Skewed Population RPS\n
                            [3] Multi-Turn RPS\n
    --data_delay/-dd:   Number of iterations between generating data.\n
                            Default is 10\n
    """
    if kwargs.get("file"):
        params = read_file()
    else:
        params = kwargs

    game_choice = params.get("game_choice", None)
    if game_choice is None:
        raise RuntimeError("No Game Selected")
    game_choice = int(game_choice)

    num_games = params.get("num_games", None)
    num_players = params.get("num_players", None)
    proportions = params.get("-p", None)
    data_delay = params.get("data_delay", None)
    ladder_choice = int(params.get("ladder", None))
    num_rounds = params.get("num_rounds", None)

    if not proportions and (game_choice == 2 or game_choice == 3):
        raise RuntimeError("No proportions specified.")

    if game_choice == 0:
        cf_sim = CFSimulation(num_games=num_games,
                              num_players=num_players,
                              ladder_choice=ladder_choice)
        cf_sim.run()
    elif game_choice == 1:
        rps_sim = RPSSimulation(num_games=num_games,
                                num_rounds=1,
                                num_players=num_players,
                                proportions=(0.25, 0.25, 0.25, 0.25, 0),
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 2:
        rps_sim = RPSSimulation(num_games=num_games,
                                num_rounds=1,
                                num_players=num_players,
                                proportions=proportions,
                                data_delay=data_delay,
                                ladder_choice=ladder_choice)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 3:
        mtrps_sim = RPSSimulation(num_games=num_games,
                                  num_rounds=num_rounds,
                                  proportions=proportions,
                                  num_players=num_players,
                                  ladder_choice=ladder_choice,
                                  data_delay=data_delay)
        mtrps_sim.add_agents()
        mtrps_sim.init_type_log_writer()
        mtrps_sim.run()
    else:
        raise RuntimeError("Invalid Game Choice")


def read_file():
    """Read CL arguments from file."""
    print("HERE!!!")
    return {}

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
