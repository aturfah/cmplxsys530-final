"""Test script for BasicPlanningPokemonAgent."""

from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from pokemon_helpers.pokemon import Pokemon
from battle_engine.pokemon_engine import anonymize_gamestate_helper


def test_generate_possibilities():
    """Test function to generate possible player and opponent moves."""
    spinda = Pokemon(name="spinda", moves=["tackle"])
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    exploud = Pokemon(name="exploud", moves=["tackle"])

    gamestate = {}
    gamestate["team"] = [exploud, magikarp]
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    bppa = BasicPlanningPokemonAgent(tier="pu", team=[spinda])
    bppa.update_gamestate(gamestate, opp_gamestate)
    player_opts, opp_opts = bppa.generate_possibilities()

    assert len(player_opts) == 3
    assert ("SWITCH", 0) in player_opts
    assert ("ATTACK", 0) in player_opts
    assert len(opp_opts) == 6
    assert ("SWITCH", "exploud") in opp_opts
    assert ("SWITCH", "magikarp") in opp_opts
    assert ("ATTACK", "return") in opp_opts

test_generate_possibilities()
