"""Test for pokemon module."""

from pokemon.pokemon import Pokemon


def test_init():
    """Test that the initialization runs well with no errors."""
    Pokemon("spinda", ["tackle"], level=50)


def test_param_validation():
    """Test that parameter validation."""
    # Invalid pokemon choice
    try:
        Pokemon("doot", ["tackle"], level=100)
        assert False
    except AttributeError:
        pass

    # No moves provided
    try:
        Pokemon("exploud", [], level=100)
        assert False
    except AttributeError:
        pass

    # Invalid moves provided
    try:
        Pokemon("exploud", ["doot"], level=100)
        assert False
    except AttributeError:
        pass

    # Level less than threshold
    try:
        Pokemon("exploud", ["tackle"], level=-1)
        assert False
    except AttributeError:
        pass

    # Level greater than threshold
    try:
        Pokemon("exploud", ["tackle"], level=500)
        assert False
    except AttributeError:
        pass

    # Level is decimal
    try:
        Pokemon("exploud", ["tackle"], level=50.5)
        assert False
    except AttributeError:
        pass

    # Invalid nature
    try:
        Pokemon("exploud", ["tackle"], nature="doot")
        assert False
    except AttributeError:
        pass


def test_stats_calculation():
    """Test that stats are calculated properly with and without natures."""
    pkmn = Pokemon("spinda", ["tackle"], level=50)
    assert pkmn.max_hp == 120
    assert pkmn.attack == 65
    assert pkmn.defense == 65
    assert pkmn.sp_attack == 65
    assert pkmn.sp_defense == 65
    assert pkmn.speed == 65

    pkmn2 = Pokemon("spinda", ["tackle"], level=50, nature="adamant")
    assert pkmn2.max_hp == 120
    assert pkmn2.attack == 71
    assert pkmn2.defense == 65
    assert pkmn2.sp_attack == 58
    assert pkmn2.sp_defense == 65
    assert pkmn2.speed == 65


test_init()
test_param_validation()
test_stats_calculation()
