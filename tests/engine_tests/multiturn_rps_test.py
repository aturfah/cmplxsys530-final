"""Test script for MTRPS Engine."""

from agent.rps_agent import RPSAgent
from battle_engine.multiturn_rps import MTRPSEngine


def test_init():
    MTRPSEngine()


def test_param_validation():
    try:
        MTRPSEngine(num_games=2)
        assert False
    except AttributeError:
        pass

    try:
        MTRPSEngine(num_games=-1)
        assert False
    except AttributeError:
        pass

    try:
        MTRPSEngine(num_games=0)
        assert False
    except AttributeError:
        pass


test_init()
test_param_validation()
