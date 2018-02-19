"""Test script for MTRPS Engine."""

from agent.rps_agent import RPSAgent
from battle_engine.multiturn_rps import MTRPSEngine

def test_init():
    mtrps = MTRPSEngine()
    rps_player1 = RPSAgent(strategy_in="rock")
    rps_player2 = RPSAgent(strategy_in="paper")

    mtrps.run(rps_player1, rps_player2)


test_init()