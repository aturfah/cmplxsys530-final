""" Script to test functioning of ladder """

from agent.base_agent import Base_Agent
from ladder.ladder import Ladder


def test_add():
    lad = Ladder()
    ba1 = Base_Agent()
    ba2 = Base_Agent()
    lad.add_player(ba1)
    lad.add_player(ba2)

test_add()