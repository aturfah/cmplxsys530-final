""" Script to run a ladder simulation for CoinFlipEngine """

from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import Base_Agent
from ladder.ladder import Ladder

def run(num_runs, num_players, suppress_print):
    game = CoinFlipEngine()    
    lad = Ladder()

    for _ in range(num_players):
        player = Base_Agent()
        lad.add_player(player)

    for _ in range(num_runs):
        lad.run_game(game)
    
    players = lad.get_players(sort=True)

    if not suppress_print:
        for player in players:
            player.print_info()
