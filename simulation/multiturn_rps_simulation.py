"""Simulation class for MultiTurn RPS Simulation."""

from math import ceil

from agent.rps_agent import RPSAgent
from agent.counter_rps_agent import CounterRPSAgent

from battle_engine.multiturn_rps import MTRPSEngine
from simulation.rps_simulation import RPSSimulation

class MTRPSSimulation(RPSSimulation):
    """Simulation for a multi-turn RPS Simulation."""
    
    def __init__(self, **kwargs):
        """Init method."""
        mtrps_kwargs = kwargs
        mtrps_kwargs["game"] = MTRPSEngine()
        mtrps_kwargs["prefix"] = "MTRPS"
        super().__init__(mtrps_kwargs)

        self.proportions = [0.3, 0.3, 0.3, 0, 0.1]

        self.add_agents()
        self.init_type_log_writer()

    def add_agents(self):
        """Add agents in specified proportions to the ladder."""
        num_rock = ceil(float(self.proportions[0])*self.num_players)
        num_paper = ceil(float(self.proportions[1])*self.num_players)
        num_scissors = ceil(float(self.proportions[2])*self.num_players)
        num_mixed = ceil(float(self.proportions[3])*self.num_players)
        num_counter = ceil(float(self.proportions[4])*self.num_players)

        for rock_ind in range(num_rock):
            agent_id = 'rock_{}'.format(rock_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='rock')
            self.ladder.add_player(player)

        for paper_ind in range(num_paper):
            agent_id = 'paper_{}'.format(paper_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='paper')
            self.ladder.add_player(player)

        for sciss_ind in range(num_scissors):
            agent_id = 'scissors_{}'.format(sciss_ind)
            player = RPSAgent(id_in=agent_id, strategy_in='scissors')
            self.ladder.add_player(player)

        for mixed_ind in range(num_mixed):
            agent_id = 'mixed_{}'.format(mixed_ind)
            player = RPSAgent(id_in=agent_id)
            self.ladder.add_player(player)
        
        for counter_ind in range(num_counter):
            agent_id = 'counter_{}'.format(counter_ind)
            player = CounterRPSAgent(id_in=agent_id)
            self.ladder.add_player(player)


    def run(self):
        """Run this simulation"""
        print("RUNNING MTRPSSimulation.")
