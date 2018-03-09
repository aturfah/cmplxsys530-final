"""Unit tests for damage_stats calculator."""

from pokemon.damage_stats import DamageStatCalc

def test_init():
    """Make sure everything initializes properly."""
    dsc = DamageStatCalc()
    assert dsc.damage_stats

test_init()
