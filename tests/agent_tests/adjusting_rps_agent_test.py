"""Test for AdjustingRPSAgent."""

from agent.adjusting_rps_agent import AdjustingRPSAgent


def test_init():
    """Test Initialization method."""
    # Test that initializes default
    arps = AdjustingRPSAgent()
    assert arps.weight == 1
    assert arps.original_strategy == arps.strategy
    assert arps.counts == [1/3, 1/3, 1/3]

    test_init_weights()


def test_init_weights():
    """Tests weights formatting of initialization."""
    # Tests when weights are not defaults
    arps_int = AdjustingRPSAgent(weight=6)
    assert arps_int.weight == 6
    assert arps_int.counts == [2, 2, 2]

    # Test non-integer weights
    arps_float = AdjustingRPSAgent(weight=2)
    assert arps_float.weight == 2
    assert arps_float.counts == [2/3, 2/3, 2/3]


test_init()
