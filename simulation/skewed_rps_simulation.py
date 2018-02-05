""" Script to run a ladder simulation for Rock Paper Scissors """

from math import ceil

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPS_Agent
from ladder.ladder import Ladder

def run(num_runs, num_players, proportions):
    game = RPSEngine()
    lad = Ladder()

    prop_rock = float(proportions[0])
    prop_paper = float(proportions[1])
    prop_scissors = float(proportions[2])

    num_rock = ceil(prop_rock*num_players)
    num_paper = ceil(prop_paper*num_players)
    num_scissors = ceil(prop_scissors*num_players)


    for i in range(num_rock):
        player = RPS_Agent('rock')
        lad.add_player(player)

    for i in range(num_paper):
        player = RPS_Agent('paper')
        lad.add_player(player)

    for i in range(num_scissors):
        player = RPS_Agent('scissors')
        lad.add_player(player)

    for i in range(num_runs):
        lad.run_game(game)
    
    players = lad.get_players(sort=True)

    for player in players:
        print("Player: {}:".format(player.id))
        print("\tElo: {}".format(player.elo))
        print("\tStrategy: {}".format(player.strategy))
        print("\tW/L Ratio: {} ({})".format(player.win_loss_ratio(), player.num_wins + player.num_losses))
