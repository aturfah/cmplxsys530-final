"""Unit tests for pokemon engine."""

from agent.pokemon_agent import PokemonAgent
from agent.pokemon.pokemon import Pokemon
from battle_engine.pokemon import PokemonEngine


def test_run():
    """Test running of a pokemon game."""
    exploud = Pokemon("exploud", ["tackle"])
    floatzel = Pokemon("floatzel", ["watergun"])
    elec_floatzel = Pokemon("floatzel", ["thundershock"])
    spinda = Pokemon("spinda", ["thundershock"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([floatzel])
    player3 = PokemonAgent([elec_floatzel])
    player4 = PokemonAgent([spinda])

    p_eng = PokemonEngine()

    outcome = p_eng.run(player1, player2)
    assert outcome == 1
    print("\n")
    outcome = p_eng.run(player2, player1)
    assert outcome == 0
    print("\n")
    outcome = p_eng.run(player1, player3)
    assert outcome == 1
    print("\n")
    outcome = p_eng.run(player2, player3)
    assert outcome == 0
    print("\n")

    outcome = p_eng.run(player3, player4)
    assert outcome == 0
    print("\n")

test_run()
