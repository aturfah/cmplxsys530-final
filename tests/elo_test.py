"""Test functionality of Elo Calculations."""

from agent.base_agent import BaseAgent
from ladder.elo import elo

# Using wikipedia's example
# from https://en.wikipedia.org/wiki/Elo_rating_system


def test_drop():
    """Test that ratings drop when appropriate."""
    player1 = BaseAgent()
    player2 = BaseAgent()
    player1.elo = 1619
    player2.elo = 1609

    player1.elo = elo(player1, player2, 0)
    assert player1.elo == 1602


def test_floor():
    """Tests that ratings do not go below 1000."""
    player1 = BaseAgent()
    player2 = BaseAgent()

    player1.elo = elo(player1, player2, 0)
    assert player1.elo == 1000


def test_increase():
    """Tests that ratings increase when appropriate."""
    player1 = BaseAgent()
    player2 = BaseAgent()
    player1.elo = 1619
    player2.elo = 1609

    player2.elo = elo(player2, player1, 1)
    assert player2.elo == 1625


test_increase()
test_drop()
test_floor()
