"""Script for running Pokemon Simulation."""

from simulation.base_simulation import BaseSimulation
from battle_engine.pokemon_engine import PokemonEngine
from agent.pokemon_agent import PokemonAgent


class PokemonSimulation(BaseSimulation):
    """Class for Pokemon Simulation."""

    def __init__(self, **kwargs):
        """Initialize this simulation."""
        pkmn_kwargs = kwargs
        pkmn_kwargs["game"] = PokemonEngine()
        pkmn_kwargs["prefix"] = "PKMN"
        super().__init__(pkmn_kwargs)

        print("POKEMON SIMULATION!!!")

    def add_agents(self):
        """Add the agents to this model."""
        for _ in range(self.num_players):
            print("ADDING AGENT #{}".format(_))

    def run(self):
        """Run this simulation."""
        print("RUNNING!!!")
