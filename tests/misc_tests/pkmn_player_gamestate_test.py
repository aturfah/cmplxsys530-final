"""Testing script for the pkmn_player_gamestate class."""

from pokemon_helpers.pkmn_player_gamestate import PokemonPlayerGameState


def basic_test():
    """Test initializing and accessing of attributes."""
    ppgs = PokemonPlayerGameState()

    # Attribute lookup
    assert not ppgs.test_attr

    # Setting values in that dictionary
    ppgs.test_attr["test"] = 7
    assert ppgs.test_attr["test"]


basic_test()
