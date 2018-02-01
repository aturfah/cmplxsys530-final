""" Test functionality of Elo Calculations """

from agent.base_agent import Base_Agent
from ladder.elo import elo

# Using wikipedia's example from https://en.wikipedia.org/wiki/Elo_rating_system

def test_drop():
    playerA = Base_Agent()
    playerB = Base_Agent()
    playerA.elo = 1619
    playerB.elo = 1609

    playerA.elo = elo(playerA, playerB, 0) 
    assert(playerA.elo == 1602)

def test_floor():
    playerA = Base_Agent()
    playerB = Base_Agent()

    playerA.elo = elo(playerA, playerB, 0)
    assert(playerA.elo == 1000)

def test_increase():
    playerA = Base_Agent()
    playerB = Base_Agent()
    playerA.elo = 1619
    playerB.elo = 1609

    playerB.elo = elo(playerB, playerA, 1) 
    print(playerB.elo)
    assert(playerB.elo == 1625)

test_increase()
test_drop()
test_floor()