"""Test for AdjustingRPSAgent."""

from agent.adjusting_rps_agent import AdjustingRPSAgent


def test_init():
    """Test Initialization method."""
    # Test that initializes default
    arps = AdjustingRPSAgent()
    assert arps.weight == 1
    assert arps.original_strategy == arps.strategy
    assert arps.counts == [1/3, 1/3, 1/3]

    # Tests when weights are not defaults
    arps_weight = AdjustingRPSAgent(weight=6)
    assert arps_weight.weight == 6
    assert arps_weight.counts == [2, 2, 2]


test_init()
