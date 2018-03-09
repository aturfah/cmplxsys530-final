"""Unit tests for damage_stats calculator."""

from pokemon.damage_stats import DamageStatCalc

def test_init():
    """Make sure everything initializes properly."""
    dsc = DamageStatCalc()
    assert dsc.damage_stats

def test_nearest_num():
    """Make sure it calculates the nearest number properly."""
    dsc = DamageStatCalc()

    assert dsc.find_closest_level(4) == (5, -1)
    assert dsc.find_closest_level(215) == (200, 15)
    assert dsc.find_closest_level(17) == (15, 2)

test_init()
test_nearest_num()
