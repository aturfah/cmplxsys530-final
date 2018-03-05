"""Unit tests for PokemonAgent class."""

from pokemon.pokemon import Pokemon
from agent.pokemon_agent import PokemonAgent

def test_make_move():
    """Test that make_move is outputting valid info."""
    spinda = Pokemon("spinda", ["tackle", "watergun", "thundershock", "shadowball"])
    magikarp = Pokemon("magikarp", ["tackle", "watergun", "thundershock", "shadowball"])
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

test_make_move()