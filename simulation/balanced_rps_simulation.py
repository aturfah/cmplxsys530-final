""" Script to run a ladder simulation for Rock Paper Scissors """

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPS_Agent
from ladder.ladder import Ladder

def run(num_runs, num_players):
    game = RPSEngine()
    
    lad = Ladder()

    for _ in range(num_players):
        player = RPS_Agent()
        lad.add_player(player)

    for _ in range(num_runs):
        lad.run_game(game)
    
    players = lad.get_players(sort=True)

    for player in players:
        player.print_info()