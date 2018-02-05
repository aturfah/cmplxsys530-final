""" Script to run a ladder simulation for CoinFlipEngine """

from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import Base_Agent
from ladder.ladder import Ladder

def run(num_runs, num_players):
    game = CoinFlipEngine()    
    lad = Ladder()

    for i in range(num_players):
        player = Base_Agent()
        lad.add_player(player)

    for i in range(num_runs):
        lad.run_game(game)
    
    players = lad.get_players(sort=True)

    for player in players:
        print("Player: {}:".format(player.id))
        print("\tElo: {}".format(player.elo))
        print("\tW/L Ratio: {} ({})".format(player.win_loss_ratio(), player.num_wins + player.num_losses))
