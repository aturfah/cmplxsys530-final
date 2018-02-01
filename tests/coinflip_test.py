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
    """ Run single iteration of game, make sure ratings update """
    player1 = Base_Agent()
    player2 = Base_Agent()

    cfe = CoinFlipEngine(player1, player2)
    cfe.run()

    assert(player1.elo != 1000 or player2.elo != 1000)
    assert(player1.num_wins != 0 or player2.num_wins != 0)
    assert(player1.num_losses != 0 or player2.num_losses != 0)

test_init()
test_run()