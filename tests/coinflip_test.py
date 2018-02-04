""" Test functionality of Coinflip Engine """
from agent.base_agent import Base_Agent
from battle_engine.coinflip import CoinFlipEngine


def test_init():
    player1 = Base_Agent()
    player2 = Base_Agent()

    # Try to initialize CoinFlipEngine with negative probability
    try:
        cfe = CoinFlipEngine(player1, player2, -1)
        assert(False)
    except AttributeError:
        pass

    # Try to initialize CoinFlipEngine with probability > 1
    try:
        cfe = CoinFlipEngine(player1, player2, 50)
        assert(False)
    except AttributeError:
        pass


def test_run():
    """ Run single iteration of game """
    player1 = Base_Agent()
    player2 = Base_Agent()

    cfe = CoinFlipEngine(prob_win = 1)
    outcome = cfe.run(player1, player2)
    assert(outcome == 1)

    cfe2 = CoinFlipEngine(prob_win= 0)
    outcome = cfe.run(player1, player2)
    assert(outcome == 0)

test_init()
test_run()
