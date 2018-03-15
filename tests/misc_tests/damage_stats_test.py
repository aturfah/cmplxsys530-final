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


def test_estimate_dmg_val():
    """Test calculation of stats."""
    dsc = DamageStatCalc()

    assert dsc.estimate_dmg_val(77) == 9.05
    assert dsc.estimate_dmg_val(144, is_hp=True) == 20.43
    assert dsc.estimate_dmg_val(88, is_atk=True) == 40.4
    assert dsc.estimate_dmg_val(150,
                                is_atk=True,
                                max_evs=True,
                                positive_nature=True) == 83.6
    assert dsc.estimate_dmg_val(90, is_hp=True) == 15.29
    assert dsc.estimate_dmg_val(120) == 13.14

def test_dmg_range():
    """Test calculation of the damage range."""
    pass

test_init()
test_nearest_num()
test_estimate_dmg_val()
test_dmg_range()