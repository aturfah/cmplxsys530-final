"""Testing script for the pkmn_player_gamestate class."""

from pokemon_helpers.pkmn_player_gamestate import PokemonPlayerGameState


def basic_test():
    """Test initializing and accessing of attributes."""
    ppgs = PokemonPlayerGameState()
    assert ppgs.test


basic_test()
