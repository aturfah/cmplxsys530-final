"""Test for AdjustingRPSAgent."""

from config import set_logging_level
from agent.adjusting_rps_agent import AdjustingRPSAgent


def test_init():
    """Test Initialization method."""
    # Test that initializes default
    arps = AdjustingRPSAgent()
    assert arps.weight == 1
    assert arps.original_strategy == arps.strategy
    assert arps.counts == [1/3, 1/3, 1/3]

    # Tests when weights are not defaults
    arps_int = AdjustingRPSAgent(weight=6)
    assert arps_int.weight == 6
    assert arps_int.counts == [2, 2, 2]

    # Test non-integer weights
    arps_float = AdjustingRPSAgent(weight=2)
    assert arps_float.weight == 2
    assert arps_float.counts == [2/3, 2/3, 2/3]

    # Test that non-standard strategy set properly
    arps_nstd = AdjustingRPSAgent(strategy_in="rock")
    assert arps_nstd.weight == 1
    assert arps_nstd.counts == [1, 0, 0]

    # Test that strategy plays nicely with weight
    arps_nstd_weight = AdjustingRPSAgent(strategy_in="rock", weight=5)
    assert arps_nstd_weight.counts == [5, 0, 0]


def test_update_info_and_reset():
    """Test that update_info works properly, as does resetting."""
    # Test updating with default parameters
    arps = AdjustingRPSAgent()
    assert arps.strategy == [1/3, 1/3, 1/3]

    arps.update_info(opp_move=0)
    assert arps.counts == [1/3, 4/3, 1/3]
    assert arps.original_strategy == [1/3, 1/3, 1/3]
    assert [round(prob, 4) for prob in arps.strategy] == [0.1667, 0.6667, 0.1667]

    arps.reset_state()
    assert arps.strategy == [1/3, 1/3, 1/3]
    assert arps.counts == [1/3, 1/3, 1/3]

    # Make sure that weights are accounted for
    arps_weight = AdjustingRPSAgent(weight=9)

    arps_weight.update_info(opp_move=1)
    assert arps_weight.counts == [3, 3, 4]
    assert arps_weight.strategy == [0.3, 0.3, 0.4]

    arps_weight.reset_state()
    assert arps_weight.strategy == [1/3, 1/3, 1/3]
    assert arps_weight.counts == [3, 3, 3]

set_logging_level()

test_init()
test_update_info_and_reset()
