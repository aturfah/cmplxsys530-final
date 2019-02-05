"""Test script for Moves."""

from pokemon_helpers.moves import BaseMove


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

test_base_init()
test_brakcet_op()
