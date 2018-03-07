"""Unit tests for PokemonAgent class."""

from pokemon.pokemon import Pokemon
from agent.pokemon_agent import PokemonAgent
from battle_engine.pokemon_engine import anonymize_gamestate_helper


def test_make_move():
    """Test that make_move is outputting valid info."""
    spinda = Pokemon(
        name="spinda",
        moves=["tackle", "watergun", "thundershock", "shadowball"])
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([spinda, magikarp, magikarp, magikarp])

    # Set player's gamestate
    pa1.gamestate = {}
    pa1.gamestate["team"] = [magikarp, magikarp, magikarp]
    pa1.gamestate["active"] = spinda

    move_type, val = pa1.make_move()

    assert move_type in ["SWITCH", "ATTACK"]
    if move_type == "SWITCH":
        # Switch to magikarp
        assert val in range(3)
    else:
        # Picks one of 4 moves
        assert val in range(4)


def test_opp_gamestate():
    """Test that opponent's gamestate is updated properly."""
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([spinda])
    pa2 = PokemonAgent([spinda])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    pa1.update_gamestate(gamestate, opp_gamestate)
    pa2.update_gamestate(gamestate, opp_gamestate)

    # Gamestate updating happens properly.
    assert pa1.opp_gamestate["data"]
    assert not pa1.opp_gamestate["data"]["team"]
    assert pa1.opp_gamestate["data"]["active"]["name"] == "spinda"

    turn_info = {}
    turn_info["attacker"] = "player2"
    turn_info["move"] = spinda.moves[0]
    turn_info = [turn_info]

    # Give new info
    pa1.new_info(turn_info, "player1")
    # New info is stored properly
    assert len(pa1.opp_gamestate["moves"]["spinda"]) == 1

    # Assert that reseting the gamestate actually does it
    pa2.reset_gamestates()
    assert not pa2.gamestate
    assert not pa2.opp_gamestate["data"]
    assert not pa2.opp_gamestate["moves"]


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


def test_battle_posn():
    """Test battle position functions work."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    magikarp_opp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([magikarp])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp

    opp_gamestate = {}
    opp_gamestate["team"] = []
    opp_gamestate["active"] = magikarp_opp
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate)

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


test_make_move()
test_opp_gamestate()
test_switch_faint()
test_battle_posn()
