"""Test script for Moves."""

from pokemon_helpers.moves import BaseMove
from pokemon_helpers.pokemon import Pokemon

from config import MOVE_DATA


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


test_base_init()
test_brakcet_op()
test_calculate_damage()
test_calculate_modifier()
test_check_hit()
