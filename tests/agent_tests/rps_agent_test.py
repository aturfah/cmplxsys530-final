"""Unit tests for Rock/Paper/Scissors agent."""

import logging

from agent.rps_agent import RPSAgent
from config import set_logging_level

def basic_test():
    """Test basic functionality."""
    # Test constructor
    rps1 = RPSAgent()
    rps_rock = RPSAgent('rock')
    rps_rock2 = RPSAgent([1, 0, 0])

    assert rps_rock.strategy == rps_rock2.strategy

    assert rps1.elo == 1000
    assert rps1.win_loss_ratio() is None


def test_validate_strategy():
    """Test invalid strategy validation."""
    try:
        RPSAgent(strategy_in='VOMIT')
        assert False
    except ValueError:
        # We should be here
        pass

    try:
        RPSAgent(strategy_in=[-1, 1, 1])
        assert False
    except ValueError:
        pass


def test_agent_type():
    """Test that agent types are properly set."""
    rps_rock = RPSAgent(strategy_in="rock")
    rps_mixed = RPSAgent(strategy_in=[1, 0, 0])

    assert rps_rock.strategy == rps_mixed.strategy
    assert rps_rock.type == "rock"
    assert rps_mixed.type == "mixed"


def test_make_move():
    """Test make_move method."""
    rps_rock = RPSAgent(id_in='rps_rock', strategy_in=[1, 0, 0])
    rps_paper = RPSAgent(id_in='rps_paper',strategy_in=[0, 1, 0])
    rps_scissors = RPSAgent(id_in='rps_scissors', strategy_in=[0, 0, 1])
    rps_random = RPSAgent(id_in='rps_random')

    assert rps_random.make_move() in [0, 1, 2]
    assert rps_rock.make_move() == 0
    assert rps_paper.make_move() == 1
    assert rps_scissors.make_move() == 2


set_logging_level(logging.DEBUG)

basic_test()
test_validate_strategy()
test_agent_type()
test_make_move()
