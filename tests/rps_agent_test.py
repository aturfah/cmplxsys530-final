""" Unit tests for Rock/Paper/Scissors agent """

from agent.rps_agent import RPS_Agent


def basic_test():
    """ Test basic functionality """
    # Test constructor
    rps1 = RPS_Agent()
    rps_rock = RPS_Agent('rock')
    rps_rock2 = RPS_Agent([1, 0, 0])

    assert(rps_rock.strategy == rps_rock2.strategy)

    error = False
    try:
        RPS_Agent(strategy_in='VOMIT')
    except ValueError:
        # We should be here
        error = True
    assert(error)  # Invalid strategy input

    error = False
    try:
        RPS_Agent(strategy_in=[1, 1, 1])
    except ValueError:
        error = True
    assert(error)  # Strategies cannot sum to 1

    error = False
    try:
        RPS_Agent(strategy_in=[-1, 1, 1])
    except ValueError:
        error = True
    assert(error)  # No negative strategies

    assert(rps1.elo == 1000)
    assert(rps1.win_loss_ratio() is None)


def test_make_move():
    """ Test make_move method """
    rps_rock = RPS_Agent(strategy_in=[1, 0, 0])
    rps_paper = RPS_Agent(strategy_in=[0, 1, 0])
    rps_scissors = RPS_Agent(strategy_in=[0, 0, 1])
    rps_random = RPS_Agent()

    assert(rps_random.make_move() in [0, 1, 2])
    assert(rps_rock.make_move() == 0)
    assert(rps_paper.make_move() == 1)
    assert(rps_scissors.make_move() == 2)


basic_test()
test_make_move()
