""" Script to run a ladder simulation """
import click

from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import Base_Agent
from ladder.ladder import Ladder

@click.command()
@click.option('--num_runs', default=5000, help='Number of games to simulate')
@click.option('--num_players', default=10, help='Number of agents')
@click.option('--game_choice', default=0, help='Which game to play. Options are:\n\t [0] coin_flip')
def run(num_runs, num_players, game_choice):
    print("Hello World!")
    game = None
    if game_choice == 0:
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

if __name__ == "__main__":
    run()
