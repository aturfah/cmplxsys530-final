"""Script to run a ladder simulation for CoinFlipEngine."""

from simulation.base_simulation import BaseSimulation
from battle_engine.coinflip import CoinFlipEngine
from agent.base_agent import BaseAgent


class CFSimulation(BaseSimulation):
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
