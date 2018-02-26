"""Unit tests for pokemon engine."""

from agent.pokemon_agent import PokemonAgent
from agent.pokemon.pokemon import Pokemon
from battle_engine.pokemon import PokemonEngine

def test_run():
    exploud = Pokemon("exploud", ["tackle"])
    floatzel = Pokemon("floatzel", ["watergun"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([floatzel])

    p_eng = PokemonEngine()

    p_eng.run(player1, player2)

test_run()