"""Testing script for the pkmn_player_gamestate class."""

from pokemon_helpers.pokemon import Pokemon
from pokemon_helpers.pkmn_player_gamestate import PokemonPlayerGameState


def basic_test():
    """Test initializing and accessing of attributes."""
    ppgs = PokemonPlayerGameState()

    # Attribute lookup
    assert not ppgs.test_attr

    # Setting values in that dictionary
    ppgs.test_attr["test"] = 7
    assert ppgs.test_attr
    assert ppgs.test_attr["test"] == 7


def test_reset_gamestates():
    """Test that resetting a gamestate works."""
    ppgs = PokemonPlayerGameState()

    # Set the values in the gamestate
    ppgs.gamestate["doot"] = 7
    ppgs.opp_gamestate["data"]["pew"] = 71

    assert ppgs.gamestate
    assert ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]
    assert not ppgs.opp_gamestate["investment"]

    # Now reset them
    ppgs.reset_gamestates()
    assert not ppgs.gamestate
    assert not ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]
    assert not ppgs.opp_gamestate["investment"]

def test_init_opp_gamestate():
    """Test that initializing an opponent's gamestate works."""
    ppgs = PokemonPlayerGameState()

    # Initialize opponent's gamestate
    spinda = Pokemon(name="spinda", moves=["tackle"])
    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda
    ppgs.init_opp_gamestate(gamestate["team"], gamestate["active"])

    # Assert that only investment was calculated
    assert ppgs.opp_gamestate["investment"]
    assert not ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]

    # Assert that values were filled in properly
    assert ppgs.opp_gamestate["investment"]["spinda"]["hp"]
    assert [int(x) for x in ppgs.opp_gamestate["investment"]["spinda"]["spe"]] == [140, 240]

basic_test()
test_reset_gamestates()
test_init_opp_gamestate()
