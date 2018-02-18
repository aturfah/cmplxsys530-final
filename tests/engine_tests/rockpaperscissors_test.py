"""Test for RPS Engine."""

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent


def test_run_game():
    """Test RPS Game executes properly."""
    rps_engine = RPSEngine(bias=1)
    rps_paper = RPSAgent(strategy_in="paper")
    rps_rock1 = RPSAgent(strategy_in="rock")
    rps_rock2 = RPSAgent(strategy_in="rock")

    assert rps_engine.run(rps_paper, rps_rock1) == 1
    assert rps_engine.run(rps_rock1, rps_paper) == 0
    assert rps_engine.run(rps_rock1, rps_rock2) == 1


test_run_game()
