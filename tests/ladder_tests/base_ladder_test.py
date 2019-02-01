"""Test for functions of BaseLadder."""

from agent.base_agent import BaseAgent
from ladder.base_ladder import BaseLadder


def test_add():
    """Basic test for ladder add_player method."""
    lad = BaseLadder()
    ba1 = BaseAgent()
    ba2 = BaseAgent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    assert len(lad.player_pool) == 2


def test_no_duplicates():
    """Test that same player cannot exist twice on ladder."""
    lad = BaseLadder()
    ba1 = BaseAgent()
    lad.add_player(ba1)

    try:
        lad.add_player(ba1)
    except ValueError:
        # Ladder throws a ValueError if a duplicate player exists
        # We want to be here
        return

    assert False


def test_selection_size():
    """Test that selection size works properly."""
    # Initialization
    lad = BaseLadder(selection_size=5)
    assert lad.selection_size == 5

    lad = BaseLadder()
    assert lad.selection_size == 1


test_add()
test_no_duplicates()
test_selection_size()
