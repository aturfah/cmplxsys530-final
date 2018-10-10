"""Testing script for the pkmn_player_gamestate class."""

def basic_test():
    """Test initializing and accessing of attributes."""
    ppgs = PokemonPlayerGameState()
    assert ppgs.test
    print(ppgs["test"])

basic_test()
