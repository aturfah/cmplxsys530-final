"""Test functionality of Coinflip Engine."""
from agent.base_agent import BaseAgent
from battle_engine.coinflip import CoinFlipEngine


def test_init():
    """Test CFE engine init method."""
    # Try to initialize CoinFlipEngine with negative probability
    try:
        cfe = CoinFlipEngine(prob_win=-1)
        assert False
    except AttributeError:
        pass

    # Try to initialize CoinFlipEngine with probability > 1
    try:
        cfe = CoinFlipEngine(prob_win=50)
        assert False
    except AttributeError:
        pass


def test_run():
    """Run single iteration of game."""
    player1 = BaseAgent()
    player2 = BaseAgent()

    cfe_win = CoinFlipEngine(prob_win=1)
    outcome = cfe_win.run(player1, player2)
    assert outcome == 1

    cfe_loss = CoinFlipEngine(prob_win=0)
    outcome = cfe_loss.run(player1, player2)
    assert outcome == 0


test_init()
test_run()
