""" Unit tests for Rock/Paper/Scissors agent """

from agent.rps_agent import RPS_Agent


def basic_test():
    """ Test basic functionality """
    rps1 = RPS_Agent()

    rps1.hello()
    print(rps1.win_loss_ratio())

basic_test()
