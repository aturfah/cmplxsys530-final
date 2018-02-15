"""Test for functions of BaseLadder."""

from agent.base_agent import BaseAgent
from ladder.base_ladder import BaseLadder
from battle_engine.coinflip import CoinFlipEngine


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


test_add()
test_no_duplicates()
