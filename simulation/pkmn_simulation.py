"""Script for running Pokemon Simulation."""

from simulation.base_simulation import BaseSimulation
from battle_engine.pokemon_engine import PokemonEngine
from agent.pokemon_agent import PokemonAgent
from pokemon_helpers.pokemon import Pokemon

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
        for ind in range(self.num_players):
            if ind % 3 == 0:
                pkmn_agent = PokemonAgent(default_team_exploud())
                pkmn_agent.type = "exploud"
            elif ind % 3 == 1:
                pkmn_agent = PokemonAgent(default_team_floatzel())
                pkmn_agent.type = "floatzel"
            else:
                pkmn_agent = PokemonAgent(default_team_spinda())
                pkmn_agent.type = "spinda"
            self.ladder.add_player(pkmn_agent)
            print("ADDING AGENT {}".format(pkmn_agent.type))

    def run(self):
        """Run this simulation."""
        for _ in range(self.num_games):
            outcome, player1, player2 = self.ladder.run_game()
            self.write_player_log(outcome, player1, player2)

def default_team_exploud():
    """Generate an Exploud for these players."""
    return [Pokemon(name="exploud", moves=["tackle"])]

def default_team_spinda():
    """Generate a Spinda for these players."""
    return [Pokemon(name="spinda", moves=["tackle"])]

def default_team_floatzel():
    """Generate a FLoatzel for the player."""
    return [Pokemon(name="floatzel", moves=["watergun"])]
