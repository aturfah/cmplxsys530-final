"""Unit tests for pokemon engine."""

from agent.basic_pokemon_agent import PokemonAgent
from pokemon_helpers.pokemon import Pokemon
from battle_engine.pokemon_engine import PokemonEngine

from config import (PAR_STATUS, PSN_STATUS, TOX_STATUS)


def test_run():
    """Test running of a pokemon game."""
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

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
    exploud = Pokemon(name="exploud", moves=["synthesis"], level=100)
    spinda1 = Pokemon(name="spinda", moves=["watergun"], level=5)
    spinda2 = Pokemon(name="spinda", moves=["tackle"], level=5)
    magikarp = Pokemon(name="magikarp", moves=["thundershock"], level=5)

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([spinda1, spinda2, magikarp])

    p_eng = PokemonEngine(turn_limit=500)

    p_eng.run(player1, player2)

    assert len(player1.game_state.opp_gamestate["moves"]["magikarp"]) == 1
    assert player1.game_state.opp_gamestate["moves"]["magikarp"][0]["name"] == "Thunder Shock"
    assert len(player1.game_state.opp_gamestate["moves"]["spinda"]) == 2


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

    p_eng = PokemonEngine(turn_limit=500)
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


def test_status_dmg():
    """Test that status_damage works properly."""
    test_burn_dmg()
    test_poison_dmg()
    test_toxic_dmg()


def test_burn_dmg():
    """Test that burn damage is applied."""
    exploud = Pokemon(name="exploud", moves=["synthesis"])
    exploud_brn = Pokemon(name="exploud", moves=["synthesis"])
    exploud_brn.status = "brn"

    player_move = ("ATTACK", 0)
    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([exploud_brn])

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)
    p_eng.run_single_turn(player_move, player_move, player1, player2)

    assert p_eng.game_state["player2"]["active"].current_hp == \
        int(1+15*p_eng.game_state["player2"]["active"].max_hp/16)


def test_poison_dmg():
    """Test that poison damage is applied."""
    exploud = Pokemon(name="exploud", moves=["synthesis"])
    exploud_psn = Pokemon(name="exploud", moves=["synthesis"])
    exploud_psn.status = PSN_STATUS

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([exploud_psn])
    player_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)
    p_eng.run_single_turn(player_move, player_move, player1, player2)

    assert p_eng.game_state["player2"]["active"].current_hp == \
        int(1+7*p_eng.game_state["player2"]["active"].max_hp/8)


def test_toxic_dmg():
    """Toxic damage applied correctly."""
    exploud = Pokemon(name="exploud", moves=["synthesis"])
    exploud_tox = Pokemon(name="exploud", moves=["shadowball"])
    exploud_tox.status = TOX_STATUS

    player1 = PokemonAgent([exploud])
    player2 = PokemonAgent([exploud_tox])
    player_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)

    # First turn is 15/16
    p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].current_hp == \
        int(1+15*p_eng.game_state["player2"]["active"].max_hp/16)
    prev_hp = p_eng.game_state["player2"]["active"].current_hp

    # Second turn is ~13/16
    p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].current_hp == \
        int(1 + prev_hp - 2*p_eng.game_state["player2"]["active"].max_hp/16)


def test_secondary_effects():
    """Main testing driver for secondary effects."""
    test_opp_2ndary_stat_change()
    test_player_2ndary_stat_changes()
    test_2ndary_status()


def test_opp_2ndary_stat_change():
    """Test secondary effects that involve opponent's stat changes."""
    spinda = Pokemon(name="spinda", moves=["lowsweep"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    player1 = PokemonAgent([spinda])
    player2 = PokemonAgent([scyther_target])
    player_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)

    # Assert Spinda_target's at -2 SpD
    p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].boosts["spe"] == -1

    # Assert that stat doesn't get lower than -6
    for _ in range(10):
        p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].boosts["spe"] == -6

    # Test that if on damage happens, stat drops don't
    # Ex: Poison Move to Steel-Type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])
    player3 = PokemonAgent([gengar_target])

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player3)
    p_eng.run_single_turn(player_move, player_move, player1, player3)

    assert p_eng.game_state["player2"]["active"].boosts["spe"] == 0


def test_player_2ndary_stat_changes():
    """Test for secondary stat changes to self."""
    spinda = Pokemon(name="spinda", moves=["poweruppunch"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    player1 = PokemonAgent([spinda])
    player2 = PokemonAgent([scyther_target])
    player_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)

    # Assert that spinda's attack is +1
    p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player1"]["active"].boosts["atk"] == 1

    # Assert that stat doesn't get higher than +6
    for _ in range(10):
        p_eng.run_single_turn(player_move, player_move, player1, player2)
    assert p_eng.game_state["player1"]["active"].boosts["atk"] == 6

    # Test that if on damage happens, stat drops don't
    # Ex: Fighting move to Ghost-type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])
    player3 = PokemonAgent([gengar_target])

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player3)
    p_eng.run_single_turn(player_move, player_move, player1, player3)

    assert p_eng.game_state["player1"]["active"].boosts["atk"] == 0


def test_2ndary_status():
    """Status effects as secondary effect."""
    spinda = Pokemon(name="spinda", moves=["nuzzle", "inferno"])
    charizard_target = Pokemon(name="charizard", moves=["synthesis", "recover"])

    player1 = PokemonAgent([spinda])
    player2 = PokemonAgent([charizard_target])
    player_first_move = ("ATTACK", 0)

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)

    # Assert that Muk gets paralyzed
    p_eng.run_single_turn(player_first_move, player_first_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].status == PAR_STATUS

    # Assert that if there's another status effect, it
    # cannot be overwritten
    charizard_target.status = PSN_STATUS
    p_eng.initialize_battle(player1, player2)
    p_eng.run_single_turn(player_first_move, player_first_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].status == PSN_STATUS

    # Assert that the type immunities are respected
    charizard_target.status = None

    player_second_move = ("ATTACK", 1)
    p_eng.initialize_battle(player1, player2)

    p_eng.run_single_turn(player_second_move, player_second_move, player1, player2)
    assert p_eng.game_state["player2"]["active"].status is None

    # Assert that if no damage, no status effect
    trapinch_target = Pokemon(name="trapinch", moves=["synthesis"])
    player3 = PokemonAgent([trapinch_target])
    p_eng.initialize_battle(player1, player3)

    p_eng.run_single_turn(player_first_move, player_first_move, player1, player3)
    assert p_eng.game_state["player2"]["active"].status is None


def test_accuracy():
    """Test to check for accuracy being taken into account."""
    # < 0.5% chance of all the hydro pumps hitting
    num_misses = 0
    for _ in range(12):
        exploud = Pokemon(name="exploud", moves=["hydropump"])
        floatzel = Pokemon(name="floatzel", moves=["hydropump"])
        player1 = PokemonAgent([exploud])
        player2 = PokemonAgent([floatzel])

        player_move = ("ATTACK", 0)

        p_eng = PokemonEngine()
        p_eng.initialize_battle(player1, player2)
        for turn_info in p_eng.run_single_turn(player_move, player_move, player1, player2)[1]:
            if not turn_info["move_hits"]:
                num_misses += 1

    assert num_misses > 0

    # All the flamethrowers should hit
    num_misses = 0
    for _ in range(50):
        exploud = Pokemon(name="exploud", moves=["flamethrower"])
        floatzel = Pokemon(name="floatzel", moves=["flamethrower"])
        player1 = PokemonAgent([exploud])
        player2 = PokemonAgent([floatzel])

        player_move = ("ATTACK", 0)

        p_eng = PokemonEngine()
        p_eng.initialize_battle(player1, player2)
        for turn_info in p_eng.run_single_turn(player_move, player_move, player1, player2)[1]:
            if not turn_info["move_hits"]:
                num_misses += 1

    assert num_misses == 0


def test_volatile_status():
    """Test to ensure volatile statuses work."""
    test_vs_switch()
    test_primary_vs()


def test_vs_switch():
    """Test that volatile statuses are reset upon switching."""
    player1 = PokemonAgent([Pokemon(name="exploud", moves=["tackle"]),
                            Pokemon(name="spinda", moves=["tackle"])])
    player2 = PokemonAgent([Pokemon(name="floatzel", moves=["tackle"]),
                            Pokemon(name="magikarp", moves=["tackle"])])

    # Initialize the game
    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)
    p_eng.game_state["player1"]["active"].volatile_status["test"] = True
    p_eng.game_state["player2"]["active"].volatile_status["test"] = True

    # Run the switch
    player_move = ("SWITCH", 0)
    p_eng.run_single_turn(player_move, player_move, player1, player2)

    # Check volatile status reset
    assert not p_eng.game_state["player1"]["team"][0].volatile_status
    assert not p_eng.game_state["player2"]["team"][0].volatile_status


def test_primary_vs():
    """Test that primary volatileStatus is set properly."""
    player1 = PokemonAgent([Pokemon(name="spinda", moves=["confuseray"])])
    player2 = PokemonAgent([Pokemon(name="spinda", moves=["uproar"])])

    p_eng = PokemonEngine()
    p_eng.initialize_battle(player1, player2)

    player_move = ("ATTACK", 0)
    p_eng.run_single_turn(player_move, player_move, player1, player2)

    # Check volatile status applied
    assert p_eng.game_state["player2"]["active"].volatile_status
    assert p_eng.game_state["player2"]["active"].volatile_status["confusion"] == 1
    assert p_eng.game_state["player2"]["active"].volatile_status["uproar"] == 1


test_run()
test_run_multiple_moves()
test_run_multiple_pokemon()
test_run_infinite()
test_heal()
test_status_dmg()
test_secondary_effects()
test_accuracy()
test_volatile_status()
