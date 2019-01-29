"""Test for RPS Engine."""

from battle_engine.rockpaperscissors import RPSEngine
from agent.rps_agent import RPSAgent


def test_param_validation():
    """Test that invalid parameters are caught."""
    try:
        RPSEngine(num_games=2)
        assert False
    except AttributeError:
        pass

    try:
        RPSEngine(num_games=-1)
        assert False
    except AttributeError:
        pass

    try:
        RPSEngine(num_games=0)
        assert False
    except AttributeError:
        pass


def test_basic_results(rps_engine):
    """
    Test that RPS results are still valid.

    Args:
        rps_engine (RPSEngine): Engine to use for this test.

    """
    rock_player = RPSAgent(strategy_in="rock")
    paper_player = RPSAgent(strategy_in="paper")
    scissors_player = RPSAgent(strategy_in="scissors")

    # Rock beats Scissors
    rs_outcome = rps_engine.run(rock_player, scissors_player)
    assert rs_outcome == 1
    # Rock loses to Paper
    rp_outcome = rps_engine.run(rock_player, paper_player)
    assert rp_outcome == 0

    # Paper beats Rock
    pr_outcome = rps_engine.run(paper_player, rock_player)
    assert pr_outcome == 1
    # Paper loses to Scissors
    ps_outcome = rps_engine.run(paper_player, scissors_player)
    assert ps_outcome == 0

    # Scissors beats Paper
    sp_outcome = rps_engine.run(scissors_player, paper_player)
    assert sp_outcome == 1
    # Scissors loses to Rock
    sr_outcome = rps_engine.run(scissors_player, rock_player)
    assert sr_outcome == 0


test_basic_results(RPSEngine())
test_basic_results(RPSEngine(num_games=3))
test_param_validation()
