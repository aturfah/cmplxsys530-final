""" Script to test functioning of ladder """

from agent.base_agent import Base_Agent
from ladder.ladder import Ladder


def test_add():
    """ Basic test for ladder add_player method """
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()
    ba1.hello()
    ba2.hello()
    lad.add_player(ba1)
    lad.add_player(ba2)

    assert(len(lad.player_pool) == 2)


def test_no_duplicates():
    """ Test that same player cannot exist twice on ladder """
    lad = Ladder()
    ba1 = Base_Agent()
    lad.add_player(ba1)

    try:
        lad.add_player(ba1)
    except ValueError:
        # Ladder throws a ValueError if a duplicate player exists
        # We want to be here
        return

    assert(False)


def test_match():
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()

    lad.add_player(ba1)
    lad.add_player(ba2)

    player, opponent = lad.match()

    # Assert that players get removed from ladder
    assert(len(lad.player_pool) == 0)
    assert(lad.num_turns == 1)

test_add()
test_no_duplicates()
test_match()