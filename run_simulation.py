"""Script to run a ladder simulation."""
from tkinter import Tk
from tkinter.filedialog import askopenfile

import click
import yaml

from simulation.cf_simulation import CFSimulation
from simulation.rps_simulation import RPSSimulation
from simulation.pkmn_simulation import PokemonSimulation


@click.command()
@click.option("-ng", "--num_games", default=5000)
@click.option("-nr", "--num_rounds", default=3)
@click.option("-np", "--num_players", default=10)
@click.option("-g", "--game_choice")
@click.option("-dd", "--data_delay", default=10)
@click.option("-l", "--ladder", default=0)
@click.option("-f", "--file", is_flag=True)
@click.option("-ss", "--selection_size", default=1)
@click.argument("proportions", nargs=-1)
def run(**kwargs):
    """
    Run the simulation.

    Arguments are as follows:\n
    --file/-f:           Read arguments from file.\n
    --num_games/-ng:     Number of games to simulate.\n
                             Default is 5000\n
    --num_rounds/-nr:    Number of rounds ber game in Multi-Turn RPS.\n
                             Default is 3.\n
    --num_playeres/-np:  Number of agents in the simulation.\n
                             Default is 10.\n
    --proportions/-p:    Proportions for RPS Simulations.\n
                             5 Values corresponding to RPSUC respectively.\n
    --ladder/-l:         Which ladder matching to use. Options are:\n
                             [0] Weighted (default)\n
                             [1] Random\n
    --game_choice/-g:   Choice of game to play. Options are:\n
                             [0] Coin Flip\n
                             [1] Balanced Population RPS\n
                             [2] Skewed Population RPS\n
                             [3] Multi-Turn RPS\n
                             [4] Pokemon Simulation\n
    --data_delay/-dd:    Number of iterations between generating data.\n
                             Default is 10\n
    --selection_size/-s: Number of players to put in the pool for candidate\n
                             opponents. Default is 1.

    """
    if kwargs.get("file"):
        params = read_file()
        for arg in kwargs:
            if arg not in params:
                params[arg] = kwargs[arg]
    else:
        params = kwargs

    game_choice = params.get("game_choice", None)
    if game_choice is None:
        raise RuntimeError("No Game Selected")
    game_choice = int(game_choice)

    params["num_games"] = int(params.get("num_games", None))
    params["num_players"] = int(params.get("num_players", None))
    params["proportions"] = params.get("proportions", None)
    params["data_delay"] = int(params.get("data_delay", None))
    params["ladder_choice"] = int(params.get("ladder", None))
    params["num_rounds"] = int(params.get("num_rounds", None))
    params["multithread"] = int(params.get("multithread", 0))
    params["selection_size"] = int(params.get("selection_size", 1))

    if not params["proportions"] and (game_choice in [2, 3]) and not params.get("config"):
        raise RuntimeError("No proportions specified.")

    if game_choice == 0:
        cf_sim = CFSimulation(**params)
        cf_sim.run()
    elif game_choice == 1:
        params["proportions"] = (0.25, 0.25, 0.25, 0.25, 0)
        rps_sim = RPSSimulation(**params)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 2:
        params["num_rounds"] = 1
        rps_sim = RPSSimulation(**params)
        rps_sim.add_agents()
        rps_sim.init_type_log_writer()
        rps_sim.run()
    elif game_choice == 3:
        mtrps_sim = RPSSimulation(**params)
        mtrps_sim.add_agents()
        mtrps_sim.init_type_log_writer()
        mtrps_sim.run()
    elif game_choice == 4:
        pkmn_sim = PokemonSimulation(**params)
        pkmn_sim.add_agents()
        pkmn_sim.init_type_log_writer()
        pkmn_sim.run()
    else:
        raise RuntimeError("Invalid Game Choice")


def read_file():
    """Read CL arguments from file."""
    # Hide default window
    root = Tk()
    root.withdraw()
    root.update()

    c_file = askopenfile()
    if c_file is None:
        raise RuntimeError("Load Aborted")

    results = yaml.load(c_file)

    return results


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
