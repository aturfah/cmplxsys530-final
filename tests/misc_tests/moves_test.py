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
    assert tackle.calculate_modifier(exploud, floatzel) == 1.5 # STAB
    assert tackle.calculate_modifier(floatzel, regirock) == 0.5 # Not Very Effective
    assert tackle.calculate_modifier(exploud, regirock) == 0.75 # Multiply together

test_base_init()
test_brakcet_op()
test_calculate_damage()
test_calculate_modifier()
