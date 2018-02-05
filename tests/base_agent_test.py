""" Test functionality of base agent """
from agent.BaseAgent import BaseAgent


def testWinLoss():
    """ Test calculation of win/loss ratio"""
    ba1 = BaseAgent()

    # Wins with no losses has undefined w/l ratio
    ba1.num_wins = 50
    assert(ba1.win_loss_ratio() is None)

    # Losses makes the calculation valid
    ba1.num_losses = 10
    assert(ba1.win_loss_ratio() == 5)

    # num_wins + num_losses = total_games
    assert(ba1.total_games() == 60)


def testMakeMove():
    """ Tests that make_move throws an error """
    ba1 = BaseAgent()

    try:
        ba1.make_move()
    except NotImplementedError:
        return

    assert(False)


testWinLoss()
testMakeMove()
