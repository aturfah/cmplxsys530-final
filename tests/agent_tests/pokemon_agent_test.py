"""Unit tests for PokemonAgent class."""

from pokemon.pokemon import Pokemon
from agent.pokemon_agent import PokemonAgent
from battle_engine.pokemon_engine import anonymize_gamestate_helper


def test_make_move():
    """Test that make_move is outputting valid info."""
    spinda = Pokemon(
        "spinda",
        ["tackle", "watergun", "thundershock", "shadowball"])
    magikarp = Pokemon(
        "magikarp",
        ["tackle", "watergun", "thundershock", "shadowball"])
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
    spinda = Pokemon("spinda", ["tackle"])

    pa1 = PokemonAgent([spinda])
    pa2 = PokemonAgent([spinda])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

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

    pa1.new_info(turn_info, "player1")
    # New info is stored properly
    assert len(pa1.opp_gamestate["moves"]["spinda"]) == 1


test_make_move()
test_opp_gamestate()
