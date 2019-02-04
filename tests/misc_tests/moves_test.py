"""Test script for Moves."""

from pokemon_helpers.moves import BaseMove


def test_base_init():
    """Test the initialization of a BaseMove class."""
    bm1 = BaseMove()

    assert bm1.name == "Jeff"


test_base_init()
