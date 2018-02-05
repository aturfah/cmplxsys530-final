""" Unit tests for Rock/Paper/Scissors agent """

from agent.rps_agent import RPS_Agent


def basic_test():
    """ Test basic functionality """
    rps1 = RPS_Agent()

    assert(rps1.elo == 1000)
    assert(rps1.win_loss_ratio() == None)


basic_test()
