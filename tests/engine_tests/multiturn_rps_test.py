"""Test script for MTRPS Engine."""

from agent.rps_agent import RPSAgent
from battle_engine.multiturn_rps import MTRPSEngine


def test_init():
    """Test that the initializaiton works."""
    MTRPSEngine()


def test_param_validation():
    """Test that invalid parameters are caught."""
    try:
        MTRPSEngine(num_games=2)
        assert False
    except AttributeError:
        pass

    try:
        MTRPSEngine(num_games=-1)
        assert False
    except AttributeError:
        pass

    try:
        MTRPSEngine(num_games=0)
        assert False
    except AttributeError:
        pass


def test_basic_results():
    """Test that RPS results are still valid."""
    mtrps = MTRPSEngine()
    rock_player = RPSAgent(strategy_in="rock")
    paper_player = RPSAgent(strategy_in="paper")
    scissors_player = RPSAgent(strategy_in="scissors")

    # Rock beats Scissors
    rs_outcome = mtrps.run(rock_player, scissors_player)
    assert rs_outcome == 1
    # Rock loses to Paper
    rp_outcome = mtrps.run(rock_player, paper_player)
    assert rp_outcome == 0

    # Paper beats Rock
    pr_outcome = mtrps.run(paper_player, rock_player)
    assert pr_outcome == 1 
    # Paper loses to Scissors
    ps_outcome = mtrps.run(paper_player, scissors_player)
    assert ps_outcome == 0

    # Scissors beats Paper
    sp_outcome = mtrps.run(scissors_player, paper_player)
    assert sp_outcome == 1
    # Scissors loses to Rock
    sr_outcome = mtrps.run(scissors_player, rock_player)
    assert sr_outcome == 0


test_init()
test_param_validation()
test_basic_results()