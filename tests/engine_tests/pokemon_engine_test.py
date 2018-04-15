"""Unit tests for pokemon engine."""

from agent.basic_pokemon_agent import PokemonAgent
from pokemon_helpers.pokemon import Pokemon
from battle_engine.pokemon_engine import PokemonEngine


def test_run():
    """Test running of a pokemon game."""
    exploud = Pokemon(name="exploud", moves=["tackle"])
    floatzel = Pokemon(name="floatzel", moves=["watergun"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([floatzel])

    p_eng = PokemonEngine()

    outcome = p_eng.run(player1, player2)
    assert outcome == 1
    assert p_eng.game_state["player1"]["active"] is not None
    assert not p_eng.game_state["player1"]["team"]
    assert p_eng.game_state["player2"]["active"] is None
    assert not p_eng.game_state["player2"]["team"]


def test_run_multiple_pokemon():
    """Test running a game with multiple pokemon."""
    exploud = Pokemon(name="exploud", moves=["tackle"], level=95)
    spinda1 = Pokemon(name="spinda", moves=["watergun"])
    spinda2 = Pokemon(name="spinda", moves=["tackle"])
    magikarp = Pokemon(name="magikarp", moves=["thundershock"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([spinda1, spinda2, magikarp])

    p_eng = PokemonEngine()

    p_eng.run(player1, player2)
    assert p_eng.game_state["player1"]["active"] is not None
    assert p_eng.game_state["player2"]["active"] is None
    assert not p_eng.game_state["player2"]["team"]

    assert len(player1.opp_gamestate["moves"]["magikarp"]) == 1
    assert player1.opp_gamestate["moves"]["magikarp"][0]["name"] == "Thunder Shock"
    assert len(player1.opp_gamestate["moves"]["spinda"]) == 2


def test_run_multiple_moves():
    """Test running a game with multiple moves."""
    exploud = Pokemon(name="exploud", moves=["shadowball"])
    spinda = Pokemon(name="spinda",
                     moves=["watergun", "tackle", "thundershock"])

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([spinda])

    p_eng = PokemonEngine()
    p_eng.run(player1, player2)


def test_run_infinite():
    """Test running a game where it'll go on forever."""
    exploud1 = Pokemon(name="exploud", moves=["shadowball"])
    exploud2 = Pokemon(name="exploud", moves=["shadowball"])

    player1 = PokemonAgent([exploud1])
    player2 = PokemonAgent([exploud2])

    p_eng = PokemonEngine()
    p_eng.run(player1, player2)
    # We got to the turn limit
    assert p_eng.game_state["num_turns"] > p_eng.turn_limit


def test_heal():
    """Test that healing works properly."""
    ivysaur = Pokemon(name="ivysaur", moves=["synthesis"])
    floatzel = Pokemon(name="floatzel", moves=["watergun"])
    player1 = PokemonAgent([ivysaur])
    player1_move = ("ATTACK", 0)
    player2 = PokemonAgent([floatzel])
    player2_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)
    p_eng.run_single_turn(player1_move, player2_move, player1, player2)

    # Healed
    assert p_eng.game_state["player1"]["active"].current_hp == \
        p_eng.game_state["player1"]["active"].max_hp


def test_status():
    """Test that the engine does status moves properly"""
    test_speed_paralyze()


def test_speed_paralyze():
    """
    Test paralysis speed drop.
    
    Spinda should outspeed exploud and kill it.
    """
    spinda = Pokemon(name="spinda", moves=["tackle"])
    exploud = Pokemon(name="exploud", moves=["tackle"])
    spinda.current_hp = 1
    exploud.current_hp = 1
    exploud.status = "par"

    player1 = PokemonAgent([spinda])
    player2 = PokemonAgent([exploud])

    p_eng = PokemonEngine()
    p_eng.run(player1, player2)
    outcome = p_eng.win_condition_met()

    assert outcome["finished"]
    assert outcome["winner"] == 1


test_run()
test_run_multiple_moves()
test_run_multiple_pokemon()
test_run_infinite()
test_heal()
test_status()
