"""Script for running Pokemon Simulation."""

from numpy.random import uniform

from agent.basic_pokemon_agent import PokemonAgent
from battle_engine.pokemon_engine import PokemonEngine
from log_manager.log_writer import LogWriter
from pokemon_helpers.pokemon import Pokemon
from simulation.base_simulation import BaseSimulation
from stats.calc import calculate_avg_elo


class PokemonSimulation(BaseSimulation):
    """Class for Pokemon Simulation."""

    def __init__(self, **kwargs):
        """Initialize this simulation."""
        pkmn_kwargs = kwargs
        pkmn_kwargs["game"] = PokemonEngine()
        pkmn_kwargs["prefix"] = "PKMN"
        self.type_log_writer = None
        self.data_delay = kwargs["data_delay"]
        super().__init__(pkmn_kwargs)

    def add_agents(self):
        """Add the agents to this model."""
        for ind in range(self.num_players):
            if ind % 3 == 0:
                pkmn_agent = PokemonAgent(default_team_exploud())
                if uniform() < 0.5:
                    pkmn_agent.type = "exploud1"
                else:
                    pkmn_agent.type = "exploud2"
            elif ind % 3 == 1:
                pkmn_agent = PokemonAgent(default_team_floatzel())
                pkmn_agent.type = "floatzel"
            else:
                pkmn_agent = PokemonAgent(default_team_spinda())
                pkmn_agent.type = "spinda"
            self.ladder.add_player(pkmn_agent)

    def run(self):
        """Run this simulation."""
        for game_ind in range(self.num_games):
            outcome, player1, player2 = self.ladder.run_game()
            self.write_player_log(outcome, player1, player2)

            if game_ind % self.data_delay == 0:
                # Calculate the average ranking statistics
                # every <data_delay> iterations
                self.type_log_writer.write_line(calculate_avg_elo(self.ladder))

    def init_type_log_writer(self):
        """Initialize Type Average Elo LogWriter."""
        header = []
        header.append("exploud1")
        header.append("exploud2")
        header.append("spinda")
        header.append("floatzel")

        self.type_log_writer = LogWriter(header, prefix="PKMNTypes")


def default_team_exploud():
    """Generate an Exploud for these players."""
    return [Pokemon(name="exploud", moves=["tackle", "shadowball"])]


def default_team_spinda():
    """Generate a Spinda for these players."""
    return [Pokemon(name="spinda", moves=["tackle"])]


def default_team_floatzel():
    """Generate a FLoatzel for the player."""
    return [Pokemon(name="floatzel", moves=["watergun"])]
