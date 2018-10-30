"""Unit tests for CounterRPSAgent class."""

from agent.counter_rps_agent import CounterRPSAgent


def test_init():
    """Test that class initializes properly."""
    CounterRPSAgent()


def test_make_move():
    """Test logic for making moves."""
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

    opp_move_scissors = 2
    c_player.last_move = opp_move_scissors
    assert c_player.make_move() == 0


def test_reset_state():
    """Assert that last_move is reset with call to reset_state."""
    c_player = CounterRPSAgent()
    assert c_player.last_move is None

    c_player.last_move = 0
    assert c_player.last_move is not None

    c_player.reset_state()
    assert c_player.last_move is None


def test_update_info():
    """Assert that player actually updates its internal state."""
    c_player = CounterRPSAgent()
    assert c_player.last_move is None

    c_player.update_info(last_move=1)
    assert c_player.last_move == 1


test_init()
test_make_move()
test_reset_state()
test_update_info
