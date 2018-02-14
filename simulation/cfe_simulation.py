"""Script to run a ladder simulation for CoinFlipEngine."""


from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import BaseAgent
from ladder.weighted_ladder import WeightedLadder
from log_manager.log_writer import LogWriter


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
    lad = WeightedLadder(game)
    player_log_writer = init_player_log_writer()

    for _ in range(num_players):
        player = BaseAgent()
        lad.add_player(player)

    for _ in range(num_runs):
        outcome, player1, player2 = lad.run_game()

        datum = {
            "outcome": outcome,
            "player1.elo": player1.elo,
            "player2.elo": player2.elo
        }
        player_log_writer.write_line(datum)


def init_player_log_writer():
    """Initialize player data LogWriter."""
    header = []
    header.append("player1.elo")
    header.append("player2.elo")
    header.append("outcome")

    log_writer = LogWriter(header, prefix="CFEPlayers")
    return log_writer
