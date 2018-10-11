"""Unit tests for PokemonAgent class."""

from pokemon_helpers.pokemon import Pokemon
from agent.basic_pokemon_agent import PokemonAgent
from battle_engine.pokemon_engine import anonymize_gamestate_helper


def test_make_move():
    """Test that make_move is outputting valid info."""
    spinda = Pokemon(
        name="spinda",
        moves=["tackle", "watergun", "thundershock", "shadowball"])
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([spinda, magikarp, magikarp, magikarp])

    # Set player's gamestate
    pa1.game_state.gamestate = {}
    pa1.game_state.gamestate["team"] = [magikarp, magikarp, magikarp]
    pa1.game_state.gamestate["active"] = spinda

    move_type, val = pa1.make_move()

    assert move_type in ["SWITCH", "ATTACK"]
    if move_type == "SWITCH":
        # Switch to magikarp
        assert val in range(3)
    else:
        # Picks one of 4 moves
        assert val in range(4)


def test_switch_faint():
    """Test that switch_faint() picks a valid pokemon."""
    exploud = Pokemon(name="exploud", moves=["tackle"])
    pa1 = PokemonAgent([exploud])

    gamestate = {}
    gamestate["team"] = [exploud, exploud, exploud]
    gamestate["active"] = None

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    pa1.update_gamestate(gamestate, opp_gamestate)
    val = pa1.switch_faint()
    assert val in range(3)


def test_battle_posn_one():
    """Test battle position functions work."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    magikarp_opp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([magikarp])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp

    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = magikarp_opp
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)

    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 1
    assert pa1.calc_opp_position() == 1
    assert pa1.battle_position() == 1

    # We're now in a bad position
    magikarp.current_hp = 1
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() < 0.1
    assert pa1.calc_opp_position() == 1
    assert pa1.battle_position() < 1

    # Now we're in a better position.
    magikarp.current_hp = magikarp.max_hp/2
    magikarp_opp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 0.5
    assert pa1.calc_opp_position() < 0.1
    assert pa1.battle_position() > 1


def test_battle_posn_multiple():
    """Test that battle position functions work with multiple pokemon."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    magikarp_opp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([magikarp, spinda, spinda])

    gamestate = {}
    gamestate["team"] = [spinda, spinda]
    gamestate["active"] = magikarp

    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = [spinda]
    opp_gamestate_dict["active"] = magikarp_opp
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)

    # Everything maximum HP
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 3
    assert pa1.calc_opp_position() == 2
    assert pa1.battle_position() == 1.5

    # Good position, opponent has low HP
    magikarp_opp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 3
    assert pa1.calc_opp_position() < 2
    assert pa1.calc_opp_position() > 1
    assert pa1.battle_position() > 1.5
    assert pa1.battle_position() < 3

    # Bad position, we have low HP
    magikarp_opp.current_hp = magikarp_opp.max_hp
    magikarp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() < 3
    assert pa1.calc_position() > 2
    assert pa1.calc_opp_position() == 2
    assert pa1.battle_position() < 1.5
    assert pa1.calc_position() > 1


test_make_move()
test_switch_faint()
test_battle_posn_one()
test_battle_posn_multiple()
