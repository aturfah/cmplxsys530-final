"""Test functionality of base agent."""
from agent.base_agent import BaseAgent

from config import set_logging_level

def test_init():
    """Test the variables are set properly."""
    ba1 = BaseAgent(id_in="doot", type="Pew")
    assert ba1.elo == 1000
    assert ba1.id == "doot"
    assert ba1.num_wins == 0
    assert ba1.num_losses == 0
    assert ba1.type == "Pew"
    assert ba1.in_game is False


def test_win_loss():
    """Test calculation of win/loss ratio."""
    ba1 = BaseAgent()

    # Wins with no losses has undefined w/l ratio
    ba1.num_wins = 50
    assert ba1.win_loss_ratio() is None

    # Losses makes the calculation valid
    ba1.num_losses = 10
    assert ba1.win_loss_ratio() == 5

    # num_wins + num_losses = total_games
    assert ba1.total_games() == 60


def test_make_move():
    """Tests that make_move throws an error."""
    ba1 = BaseAgent()

    try:
        ba1.make_move()
        assert False
    except NotImplementedError:
        return

set_logging_level()

test_init()
test_win_loss()
test_make_move()
