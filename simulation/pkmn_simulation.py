"""Script for running Pokemon Simulation."""

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from battle_engine.pokemon_engine import PokemonEngine
from log_manager.log_writer import LogWriter
from pokemon_helpers.pokemon import default_team_floatzel
from pokemon_helpers.pokemon import default_team_ivysaur
from pokemon_helpers.pokemon import default_team_spinda
from simulation.base_type_logging_simulation import BaseLoggingSimulation


class PokemonSimulation(BaseLoggingSimulation):
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
            if ind % 3 == 1:
                pkmn_agent = PokemonAgent(default_team_floatzel())
                pkmn_agent.type = "RandomFloatzel"
            elif ind % 3 == 2:
                pkmn_agent = PokemonAgent(default_team_ivysaur())
                pkmn_agent.type = "RandomIvysaur"
            else:
                pkmn_agent = PokemonAgent(default_team_spinda())
                pkmn_agent.type = "RandomSpinda"

            self.ladder.add_player(pkmn_agent)

        for ind in range(self.num_players):
            if ind % 3 == 1:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_floatzel())
                pkmn_agent.type = "PlanningFloatzel"
            elif ind % 3 == 2:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_ivysaur())
                pkmn_agent.type = "PlanningIvysaur"
            else:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_spinda())
                pkmn_agent.type = "PlanningSpinda"
            self.ladder.add_player(pkmn_agent)

    def init_type_log_writer(self):
        """Initialize Type Average Elo LogWriter."""
        header = []
        header.append("RandomSpinda")
        header.append("RandomIvysaur")
        header.append("RandomFloatzel")
        header.append("PlanningSpinda")
        header.append("PlanningIvysaur")
        header.append("PlanningFloatzel")

        self.type_log_writer = LogWriter(header, prefix="PKMNTypes")
