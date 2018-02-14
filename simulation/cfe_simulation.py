"""Script to run a ladder simulation for CoinFlipEngine."""


from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import BaseAgent
from ladder.ladder import Ladder


def run(num_runs, num_players):
    """
    Run Coinflip Simulation.

    :param num_runs: int
        Number of games to play
    :param num_players: int
        Number of players to have in ladder player pool
    :param suppress_print: bool
        Whether or not to output the ratings at the end
    """
    game = CoinFlipEngine()
    lad = Ladder(game)

    for _ in range(num_players):
        player = BaseAgent()
        lad.add_player(player)

    for _ in range(num_runs):
        lad.run_game()
