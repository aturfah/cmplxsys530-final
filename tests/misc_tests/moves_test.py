"""Test script for Moves."""

from pokemon_helpers.pokemon import Pokemon

from pokemon_helpers.moves import BaseMove, OHKOMove, SecondaryEffectMove
from config import (MOVE_DATA, PAR_STATUS, PSN_STATUS, TOX_STATUS)


def test_base_init():
    """Test the initialization of a BaseMove class."""
    # Default initialization, everything is None
    bm1 = BaseMove(**{})
    assert bm1.num is None

    bm2 = BaseMove(**{"num": -1, "doot": "doot"})
    assert bm2.num == -1


def test_brakcet_op():
    """Test that [] works on BaseMove."""
    bm1 = BaseMove(**{})
    assert bm1.name == bm1["name"] == bm1.get("name")
    assert "name" in bm1


def test_calculate_damage():
    """Test that damage is calculated properly."""
    tackle = BaseMove(**MOVE_DATA["tackle"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

    damage, _ = tackle.calculate_damage(exploud, floatzel, True)
    assert damage == 78


def test_calculate_modifier():
    """Test that modifier is calculated properly."""
    tackle = BaseMove(**MOVE_DATA["tackle"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])
    gengar = Pokemon(name="gengar", moves=["tackle"])
    regirock = Pokemon(name="regirock", moves=["selfdestruct"])

    assert tackle.calculate_modifier(exploud, gengar) == 0  # No Effect
    assert tackle.calculate_modifier(exploud, floatzel) == 1.5  # STAB
    assert tackle.calculate_modifier(floatzel, regirock) == 0.5  # Not Very Effective
    assert tackle.calculate_modifier(exploud, regirock) == 0.75  # Multiply together


def test_check_hit():
    """Test that move accuracy is calculated properly."""
    hydro_pump = BaseMove(**MOVE_DATA["hydropump"])
    aerial_ace = BaseMove(**MOVE_DATA["aerialace"])
    sheer_cold = BaseMove(**MOVE_DATA["sheercold"])
    fire_punch = BaseMove(**MOVE_DATA["firepunch"])
    num_trials = 500

    num_hp_hits = 0
    num_sc_hits = 0
    num_aa_hits = 0
    num_fp_hits = 0
    for _ in range(num_trials):
        if hydro_pump.check_hit():
            num_hp_hits += 1
        if sheer_cold.check_hit():
            num_sc_hits += 1
        if aerial_ace.check_hit():
            num_aa_hits += 1
        if fire_punch.check_hit():
            num_fp_hits += 1

    assert num_hp_hits < num_trials  # Hydro Pump ssometimes miss (80% Accuracy)
    assert num_aa_hits == num_trials  # Aerial Ace should never miss (T/F case)
    assert num_sc_hits < num_hp_hits  # Sheer Cold should rarely hit (30% Accuracy)
    assert num_fp_hits == num_trials    # Fire Punch also shouldn't miss


def test_ohko_move():
    """Test that OHKO moves do target's current HP worth of damage."""
    sheer_cold = OHKOMove(**MOVE_DATA["sheercold"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

    assert sheer_cold.calculate_damage(exploud, floatzel)[0] == floatzel.current_hp


def test_secondary_effects():
    """Main testing driver for secondary effects."""
    test_opp_2ndary_stat_change()
    test_player_2ndary_stat_changes()
    test_2ndary_status()


def test_opp_2ndary_stat_change():
    """Test secondary effects that involve opponent's stat changes."""
    spinda = Pokemon(name="spinda", moves=["lowsweep"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    low_sweep = SecondaryEffectMove(**MOVE_DATA["lowsweep"])

    # Assert scyther is at -1 Speed
    low_sweep.apply_secondary_effect(spinda, scyther_target)
    assert scyther_target.boosts["spe"] == -1

    # Assert that stat doesn't get lower than -6
    for _ in range(10):
        low_sweep.apply_secondary_effect(spinda, scyther_target)
    assert scyther_target.boosts["spe"] == -6

    # Test that if on damage happens, stat drops don't
    # Ex: Fighting move to Ghost-type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])

    low_sweep.apply_secondary_effect(spinda, gengar_target)
    assert gengar_target.boosts["spe"] == 0


def test_player_2ndary_stat_changes():
    """Test for secondary stat changes to self."""
    spinda = Pokemon(name="spinda", moves=["poweruppunch"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    powerup_punch = SecondaryEffectMove(**MOVE_DATA["poweruppunch"])

    # Assert that spinda's attack is +1
    powerup_punch.apply_secondary_effect(spinda, scyther_target)
    assert spinda.boosts["atk"] == 1

    # Assert that stat doesn't get higher than +6
    for _ in range(10):
        powerup_punch.apply_secondary_effect(spinda, scyther_target)
    assert spinda.boosts["atk"] == 6

    # Test that if on damage happens, stat drops don't
    # Ex: Fighting move to Ghost-type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])
    spinda.boosts["atk"] = 0

    powerup_punch.apply_secondary_effect(spinda, gengar_target)
    assert spinda.boosts["atk"] == 0


def test_2ndary_status():
    """Status effects as secondary effect."""
    spinda = Pokemon(name="spinda", moves=["nuzzle", "inferno"])
    charizard_target = Pokemon(name="charizard", moves=["synthesis", "recover"])

    nuzzle = SecondaryEffectMove(**MOVE_DATA["nuzzle"])
    inferno = SecondaryEffectMove(**MOVE_DATA["inferno"])

    # Assert that Muk gets paralyzed
    nuzzle.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status == PAR_STATUS

    # Assert that if there's another status effect, it
    # cannot be overwritten
    charizard_target.status = PSN_STATUS
    nuzzle.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status == PSN_STATUS

    # Assert that the type immunities are respected
    charizard_target.status = None

    inferno.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status is None

    # Assert that if no damage, no status effect
    trapinch_target = Pokemon(name="trapinch", moves=["synthesis"])

    nuzzle.apply_secondary_effect(spinda, trapinch_target)
    assert trapinch_target.status is None

test_base_init()
test_brakcet_op()
test_calculate_damage()
test_calculate_modifier()
test_check_hit()
test_ohko_move()
test_secondary_effects()