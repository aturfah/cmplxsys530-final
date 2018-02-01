""" Test functionality of Elo Calculations """

from agent.base_agent import Base_Agent
from ladder.elo import elo

# Using wikipedia's example from https://en.wikipedia.org/wiki/Elo_rating_system

playerA = Base_Agent()
playerA.elo = 1613

# Set up adverseries 
playerB = Base_Agent()
playerB.elo = 1609
playerC = Base_Agent()
playerC.elo = 1477
playerD = Base_Agent()
playerD.elo = 1388
playerE = Base_Agent()
playerE.elo = 1586
playerF = Base_Agent()
playerF.elo = 1720

#TODO calculate the results by hand
playerA.elo = elo(playerA, playerB, 0) 
print(playerA.elo)
playerA.elo = elo(playerA, playerC, 0.5)
print(playerA.elo)
playerA.elo = elo(playerA, playerD, 1)
print(playerA.elo)
playerA.elo = elo(playerA, playerE, 1)
print(playerA.elo)
playerA.elo = elo(playerA, playerF, 0)
print(playerA.elo)

