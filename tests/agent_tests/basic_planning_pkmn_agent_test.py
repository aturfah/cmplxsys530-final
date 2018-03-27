"""Test script for BasicPlanningPokemonAgent."""

from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from pokemon_helpers.pokemon import Pokemon
from battle_engine.pokemon_engine import anonymize_gamestate_helper


def basic_test():
    """Basic Test."""
    spinda = Pokemon(name="spinda", moves=["tackle"])
    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    bppa = BasicPlanningPokemonAgent(tier="pu", team=[spinda])
    bppa.update_gamestate(gamestate, opp_gamestate)
    bppa.make_move()

basic_test()
