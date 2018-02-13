"""Script to run a ladder simulation for CoinFlipEngine."""


from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import BaseAgent
from ladder.ladder import Ladder


def run(num_runs, num_players, suppress_print):
    """Run Coinflip Simulation."""
    game = CoinFlipEngine()
    lad = Ladder(game)

    for _ in range(num_players):
        player = BaseAgent()
        lad.add_player(player)

    for _ in range(num_runs):
        lad.run_game()

    players = lad.get_players(sort=True)

    if not suppress_print:
        for player in players:
            player.print_info()
