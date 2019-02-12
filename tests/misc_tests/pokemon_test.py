"""Test for pokemon module."""

from math import floor

from config import BRN_STATUS, PAR_STATUS
from pokemon_helpers.pokemon import Pokemon


def test_init():
    """Test that the initialization runs well with no errors."""
    Pokemon(name="spinda", moves=["tackle"], level=50)


def test_param_validation():
    """Test that parameter validation."""
    pokemon_validation()
    move_validation()
    nature_validation()
    level_validation()
    ev_validation()


def move_validation():
    """Validate the moves provided."""
    # Invalid moves provided
    try:
        Pokemon(name="exploud", moves=["doot"], level=100)
        assert False
    except AttributeError:
        pass

    # No moves provided
    try:
        Pokemon(name="exploud", moves=[], level=100)
        assert False
    except AttributeError:
        pass


def nature_validation():
    """Validate nature properly handled."""
    # Invalid nature
    try:
        Pokemon(name="exploud", moves=["tackle"], nature="doot")
        assert False
    except AttributeError:
        pass


def level_validation():
    """Validate proper handling of invalid levels."""
    # Level less than threshold
    try:
        Pokemon(name="exploud", moves=["tackle"], level=-1)
        assert False
    except AttributeError:
        pass

    # Level greater than threshold
    try:
        Pokemon(name="exploud", moves=["tackle"], level=500)
        assert False
    except AttributeError:
        pass

    # Level is decimal
    try:
        Pokemon(name="exploud", moves=["tackle"], level=50.5)
        assert False
    except AttributeError:
        pass


def pokemon_validation():
    """Validate pokemon choice."""
    # Invalid pokemon choice
    try:
        Pokemon(name="doot", moves=["tackle"], level=100)
        assert False
    except AttributeError:
        pass


def ev_validation():
    """Validate provided EVs."""
    # Negative EVs
    try:
        evs = {"hp": -1, "atk": 1}
        Pokemon(name="exploud", moves=["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass

    # Too many EVs
    try:
        evs = {"hp": 500, "atk": 1}
        Pokemon(name="exploud", moves=["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass

    # Decimal EVs
    try:
        evs = {"hp": 500.5, "atk": 1}
        Pokemon(name="exploud", moves=["tackle"], evs=evs)
        assert False
    except AttributeError:
        pass


def test_stats_calculation():
    """Test that stats are calculated properly with and without natures."""
    pkmn1 = Pokemon(name="spinda", moves=["tackle"], level=50)
    assert pkmn1.max_hp == 135
    assert pkmn1.attack == 80
    assert pkmn1.defense == 80
    assert pkmn1.sp_attack == 80
    assert pkmn1.sp_defense == 80
    assert pkmn1.speed == 80

    pkmn2 = Pokemon(name="spinda",
                    moves=["tackle"], level=50, nature="adamant")
    assert pkmn2.max_hp == 135
    assert pkmn2.attack == 88
    assert pkmn2.defense == 80
    assert pkmn2.sp_attack == 72
    assert pkmn2.sp_defense == 80
    assert pkmn2.speed == 80

    evs = {}
    evs["atk"] = 252
    evs["spe"] = 56
    evs["spa"] = 56
    evs["hp"] = 128
    pkmn3 = Pokemon(name="spinda",
                    moves=["tackle"], level=50, nature="adamant", evs=evs)
    assert pkmn3.max_hp == 151
    assert pkmn3.attack == 123
    assert pkmn3.defense == 80
    assert pkmn3.sp_attack == 78
    assert pkmn3.sp_defense == 80
    assert pkmn3.speed == 87


def test_getitem_validation():
    """Test using the [] operator on this object."""
    pkmn1 = Pokemon(name="spinda", moves=["tackle"], level=50)

    assert pkmn1.level == pkmn1["level"]
    assert pkmn1.name == pkmn1["name"]
    assert pkmn1.base_stats["atk"] == pkmn1["baseStats"]["atk"]
    assert pkmn1.base_stats["atk"] == pkmn1["base_stats"]["atk"]


def test_effective_stats():
    """Test that stat boosts are calculated effectively."""
    pkmn1 = Pokemon(name="spinda", moves=["tackle"], level=50)

    # Positive boosts
    pkmn1.boosts["atk"] = 1
    assert pkmn1.effective_stat("atk") == 80*1.5
    pkmn1.boosts["atk"] = 6
    assert pkmn1.effective_stat("atk") == 80*4

    pkmn1.boosts["atk"] = -1
    assert pkmn1.effective_stat("atk") == int(80*2/3)
    pkmn1.boosts["atk"] = -6
    assert pkmn1.effective_stat("atk") == 80*2/8


def test_status():
    """Test that the pokemon's stats are affected by stats."""
    test_speed_paralyze()
    test_attack_burn()


def test_speed_paralyze():
    """
    Test paralysis speed drop.

    Paralyzed speed = 1/2 * normal speed
    """
    exploud = Pokemon(name="exploud", moves=["tackle"])
    exploud_par = Pokemon(name="exploud", moves=["tackle"])
    exploud_par.status = PAR_STATUS

    assert exploud.speed == exploud_par.speed
    assert floor(exploud.effective_stat("spe") / 2) ==\
        exploud_par.effective_stat("spe")


def test_attack_burn():
    """
    Test that the attack drop happens on burn.

    Burned attack = 1/2 * normal attack
    """
    exploud = Pokemon(name="exploud", moves=["tackle"])
    exploud_brn = Pokemon(name="exploud", moves=["tackle"])
    exploud_brn.status = BRN_STATUS

    assert exploud.attack == exploud_brn.attack
    assert floor(exploud.effective_stat("atk") / 2) ==\
        exploud_brn.effective_stat("atk")


def test_get_method():
    """Test .get() on a Pokemon."""
    pkmn = Pokemon(name="spinda", moves=["tackle"], level=50)

    assert pkmn.get("name") == "spinda"
    assert pkmn.get("DOOT") is None


def test_possible_moves():
    """Make sure possible_moves works properly."""
    pkmn = Pokemon(name="spinda", moves=["tackle", "watergun"], level=50)
    poke_can_switch, moves = pkmn.possible_moves()

    assert poke_can_switch
    assert moves
    assert len(moves) == 2


test_init()
test_param_validation()
test_stats_calculation()
test_getitem_validation()
test_effective_stats()
test_status()
test_get_method()
test_possible_moves()
