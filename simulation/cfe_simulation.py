"""Script to run a ladder simulation for CoinFlipEngine."""

from simulation.base_simulation import BaseSimulation
from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import BaseAgent


class CFESimulation(BaseSimulation):
    """Class to run Coin Flip Simulation."""

    def __init__(self, **kwargs):
        """Initialize CF Simulation."""
        cfe_kwargs = kwargs
        cfe_kwargs["game"] = CoinFlipEngine()
        cfe_kwargs["prefix"] = "CF"
        super().__init__(kwargs)

        self.add_agents()

    def add_agents(self):
        """Add agents to the ladder."""
        for _ in range(self.num_players):
            player = BaseAgent()
            self.ladder.add_player(player)

    def run(self):
        """Run the CF Simulation."""
        for _ in range(self.num_runs):
            outcome, player1, player2 = self.ladder.run_game()
            self.write_player_log(outcome, player1, player2)

def run(**kwargs):
    """
    Run Coinflip Simulation.

    :param num_runs: int
        Number of games to play
    :param num_players: int
        Number of players to have in ladder player pool
    """
    num_players = kwargs["num_players"]
    num_runs = kwargs["num_runs"]
    ladder_choice = kwargs["ladder_choice"]

    game = CoinFlipEngine()
    lad = LADDER_CHOICES[ladder_choice](game)
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
