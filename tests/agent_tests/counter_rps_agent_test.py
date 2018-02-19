"""Unit tests for CounterRPSAgent class."""

from agent.counter_rps_agent import CounterRPSAgent


def test_init():
    CounterRPSAgent()


def test_make_move():
    c_player = CounterRPSAgent()

    # Makes random move
    assert c_player.make_move() in [0, 1, 2]

    # Counters opponent's move
    opp_move_rock = 0
    c_player.last_move = opp_move_rock
    assert c_player.make_move() == 1

    opp_move_paper = 1
    c_player.last_move = opp_move_paper
    assert c_player.make_move() == 2

    opp_move_scissors = 0
    c_player.last_move = opp_move_scissors
    assert c_player.make_move() == 0


test_init()
test_make_move()
