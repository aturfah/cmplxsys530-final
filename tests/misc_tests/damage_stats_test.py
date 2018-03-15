"""Unit tests for damage_stats calculator."""

from pokemon.pokemon import Pokemon
from pokemon.damage_stats import DamageStatCalc

from config import MOVE_DATA
from config import POKEMON_DATA

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
    range_no_param()
    range_atk_param()


def range_no_param():
    """Range Calculations with no parameters."""
    dsc = DamageStatCalc()

    attacker = Pokemon(name="spinda", moves=["tackle"])
    defender = Pokemon(name="spinda", moves=["tackle"])
    move = MOVE_DATA["tackle"]
    params = {}
    params["atk"] = {}
    params["def"] = {}
    params["hp"] = {}

    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] > 16
    assert dmg_range[1] <= 20

    attacker = Pokemon(name="floatzel", moves=["watergun"])
    move = MOVE_DATA['watergun']
    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] == 21.25
    assert dmg_range[1] == 26

    defender = attacker
    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] == 10.2
    assert dmg_range[1] == 13

def range_atk_param():
    """Range calculations with attack parameters."""
    dsc = DamageStatCalc()

    attacker = POKEMON_DATA["spinda"]
    defender = POKEMON_DATA["spinda"]
    move = MOVE_DATA["tackle"]

    params = {}
    params["atk"] = {}
    params["atk"]["max_evs"] = True
    params["atk"]["positive_nature"] = True
    params["def"] = {}
    params["hp"] = {}

    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] == 24.65
    assert dmg_range[1] == 30

    attacker = POKEMON_DATA["exploud"]
    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] == 32.3
    assert dmg_range[1] == 39

    params["atk"]["positive_nature"] = False
    defender = POKEMON_DATA["floatzel"]
    dmg_range = dsc.calculate_range(move, attacker, defender, params)
    assert dmg_range[0] > 26 and dmg_range[0] < 26.351
    assert dmg_range[1] == 32


test_init()
test_nearest_num()
test_estimate_dmg_val()
test_dmg_range()
