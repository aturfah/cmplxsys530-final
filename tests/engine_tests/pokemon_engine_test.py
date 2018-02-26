"""Unit tests for pokemon engine."""

from agent.pokemon_agent import PokemonAgent
from agent.pokemon.pokemon import Pokemon
from battle_engine.pokemon import PokemonEngine


def test_run():
    """Test running of a pokemon game."""
    exploud = Pokemon("exploud", ["tackle"])
    floatzel = Pokemon("floatzel", ["watergun"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([floatzel])

    p_eng = PokemonEngine()

    outcome = p_eng.run(player1, player2)
    assert outcome == 1
    assert p_eng.game_state["player1"]["active"] is not None
    assert not p_eng.game_state["player1"]["team"]
    assert p_eng.game_state["player2"]["active"] is None
    assert not p_eng.game_state["player2"]["team"]


test_run()
