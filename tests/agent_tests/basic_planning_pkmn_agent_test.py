"""Test script for BasicPlanningPokemonAgent."""

from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from pokemon_helpers.pokemon import Pokemon
from battle_engine.pokemon_engine import anonymize_gamestate_helper

from config import PAR_STATUS


def init_bppa():
    """Initialize the Player for these tests."""
    spinda = Pokemon(name="spinda", moves=["tackle", "frustration"])
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    exploud = Pokemon(name="exploud", moves=["tackle"])

    gamestate = {}
    gamestate["team"] = [exploud, magikarp]
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    bppa = BasicPlanningPokemonAgent(tier="pu", team=[spinda])
    bppa.update_gamestate(gamestate, opp_gamestate)
    bppa.init_opp_gamestate(opp_gamestate["team"], opp_gamestate["active"])
    return bppa


def test_generate_possibilities():
    """Test function to generate possible player and opponent moves."""
    bppa = init_bppa()
    player_opts, opp_opts = bppa.generate_possibilities()

    assert len(player_opts) == 4
    assert ("SWITCH", 0) in player_opts
    assert ("ATTACK", 0) in player_opts
    assert ("ATTACK", 1) in player_opts
    assert len(opp_opts) == 6
    assert ("SWITCH", 0) in opp_opts
    assert ("SWITCH", 1) in opp_opts
    assert ("ATTACK", "return") in opp_opts


def test_make_move():
    """Test the results of make_move()."""
    bppa = init_bppa()
    move = bppa.make_move()

    # We choose Frustration not Tackle
    assert move[0] == "ATTACK"
    assert move[1] == 1


def test_determine_faster():
    """
    Test ability to determine if player faster.

    A -> Abomasnow, S -> Spinda
    Under normal conditions, A is faster.
    When A is paralyzed, S is faster.
    When S is boosted, S is faster.
    When A and S are both boosted, A is faster.
    When A and S are both boosted, and A is paralyzed, S is faster.

    """
    player_spinda = Pokemon(name="spinda", moves=["tackle"])
    opp_abomasnow = Pokemon(name="abomasnow", moves=["tackle"])

    player_move = ("ATTACK", 0)
    opp_move = ("ATTACK", "tackle")
    player_gs = {"team": [], "active": player_spinda}

    player = BasicPlanningPokemonAgent(tier="pu", team=[player_spinda])

    # Slower than regular abomasnow
    opp_gs = {"data": anonymize_gamestate_helper({"team": [], "active": opp_abomasnow})}
    player.update_gamestate(player_gs, opp_gs)
    player.init_opp_gamestate(opp_gs["data"]["team"], opp_gs["data"]["active"])
    assert not player.determine_faster(player.game_state.gamestate, opp_gs, player_move, opp_move)

    # Faster than paralyzed abonasnow
    opp_abomasnow.status = PAR_STATUS
    opp_gs = {"data": anonymize_gamestate_helper({"team": [], "active": opp_abomasnow})}
    player.update_gamestate(player_gs, opp_gs)

    assert player.determine_faster(player.game_state.gamestate, opp_gs, player_move, opp_move)

    # Faster than regular abomasnow at +6
    player_gs["active"]["boosts"]["spe"] = 6
    opp_abomasnow.status = None
    opp_gs = {"data": anonymize_gamestate_helper({"team": [], "active": opp_abomasnow})}
    player.update_gamestate(player_gs, opp_gs)
    assert player.determine_faster(player.game_state.gamestate, opp_gs, player_move, opp_move)

    # Slower than regular abomasnow when both at +6
    opp_abomasnow.boosts["spe"] = 6
    opp_gs = {"data": anonymize_gamestate_helper({"team": [], "active": opp_abomasnow})}
    player.update_gamestate(player_gs, opp_gs)
    assert not player.determine_faster(player.game_state.gamestate, opp_gs, player_move, opp_move)

    # Faster than paralyzed abomasnow when both at +6
    opp_abomasnow.status = PAR_STATUS
    opp_gs = {"data": anonymize_gamestate_helper({"team": [], "active": opp_abomasnow})}
    player.update_gamestate(player_gs, opp_gs)
    assert player.determine_faster(player.game_state.gamestate, opp_gs, player_move, opp_move)


def test_move_accuracy():
    """Test ability to 'risk' with move accuracy."""
    # Set up Pokemon
    floatzel = Pokemon(name="floatzel", moves=["tackle", "hydropump"])
    opp_stunfisk = Pokemon(name="stunfisk", moves=["discharge"])
    opp_stunfisk.current_hp = 1

    # Set up player gamestates
    player_gs = {}
    player_gs["team"] = []
    player_gs["active"] = floatzel

    opp_gs = {}
    opp_gs["team"] = []
    opp_gs["active"] = opp_stunfisk
    opp_gs = anonymize_gamestate_helper(opp_gs)

    print(player_gs)
    print(opp_gs)

    # Set up Agent
    bppa = BasicPlanningPokemonAgent(tier="pu", team=[floatzel])
    bppa.update_gamestate(player_gs, opp_gs)
    bppa.init_opp_gamestate(opp_gs["team"], opp_gs["active"])

    move = bppa.make_move()
    assert move[0] == "ATTACK"
    assert move[1] == 0

test_generate_possibilities()
test_make_move()
test_determine_faster()
test_move_accuracy()
