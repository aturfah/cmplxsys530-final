"""Test for AdjustingRPSAgent."""

from agent.adjusting_rps_agent import AdjustingRPSAgent


def test_init():
    """Test Initialization method."""
    arps = AdjustingRPSAgent()
    assert arps.weight == 3
    assert arps.original_strategy == arps.strategy
    assert arps.counts == [1, 1, 1]


test_init()
