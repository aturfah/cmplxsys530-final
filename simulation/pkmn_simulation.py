"""Script for running Pokemon Simulation."""

from threading import Thread
from queue import Queue
from time import time

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from battle_engine.pokemon_engine import PokemonEngine
from log_manager.log_writer import LogWriter
from pokemon_helpers.pokemon import default_team_floatzel
from pokemon_helpers.pokemon import default_team_ivysaur
from pokemon_helpers.pokemon import default_team_spinda
from simulation.base_type_logging_simulation import BaseLoggingSimulation
from stats.calc import calculate_avg_elo


class PokemonSimulation(BaseLoggingSimulation):
    """Class for Pokemon Simulation."""

    def __init__(self, **kwargs):
        """Initialize this simulation."""
        pkmn_kwargs = kwargs
        pkmn_kwargs["game"] = PokemonEngine()
        pkmn_kwargs["prefix"] = "PKMN"
        self.type_log_writer = None
        self.data_delay = kwargs["data_delay"]
        self.multithread = kwargs.get("multithread", False)
        super().__init__(pkmn_kwargs)

    def add_agents(self):
        """Add the agents to this model."""
        for ind in range(self.num_players):
            if ind % 3 == 1:
                pkmn_agent = PokemonAgent(default_team_floatzel())
                pkmn_agent.type = "RandomFloatzel"
            elif ind % 3 == 2:
                pkmn_agent = PokemonAgent(default_team_ivysaur())
                pkmn_agent.type = "RandomIvysaur"
            else:
                pkmn_agent = PokemonAgent(default_team_spinda())
                pkmn_agent.type = "RandomSpinda"

            self.ladder.add_player(pkmn_agent)

        for ind in range(self.num_players):
            if ind % 3 == 1:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_floatzel())
                pkmn_agent.type = "PlanningFloatzel"
            elif ind % 3 == 2:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_ivysaur())
                pkmn_agent.type = "PlanningIvysaur"
            else:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_spinda())
                pkmn_agent.type = "PlanningSpinda"
            self.ladder.add_player(pkmn_agent)

    def init_type_log_writer(self):
        """Initialize Type Average Elo LogWriter."""
        header = []
        header.append("random.spinda")
        header.append("random.ivysaur")
        header.append("random.floatzel")
        header.append("planning.spinda")
        header.append("planning.ivysaur")
        header.append("planning.floatzel")

        self.type_log_writer = LogWriter(header, prefix="PKMNTypes")

    def run(self):
        """Run this simulation."""
        if not self.multithread:
            super().run()
            return

        battle_queue = Queue()
        battle_results_queue = Queue()
        type_results_queue = Queue()
        for num in range(self.num_games):
            battle_queue.put(num)

        start_time = time()
        # Threads to run the battles
        for _ in range(4):
            battle_thread = Thread(target=battle, args=(self,
                                                        battle_queue,
                                                        battle_results_queue,
                                                        type_results_queue,
                                                        start_time))
            battle_thread.start()

        battle_queue.join()

        while not battle_results_queue.empty():
            output, player1, player2 = battle_results_queue.get()
            self.write_player_log(output, player1, player2)
            battle_results_queue.task_done()

        while not type_results_queue.empty():
            data_line = type_results_queue.get()
            self.type_log_writer.write_line(data_line)
            type_results_queue.task_done()

def battle(main_sim, battle_queue, output_queue, type_queue, start_time):
    """Code for a single battle thread to run."""
    while not battle_queue.empty():
        battle_queue.get()
        results = main_sim.ladder.run_game()
        output_queue.put(results)
        if battle_queue.qsize() % main_sim.data_delay == 0:
            type_queue.put(calculate_avg_elo(main_sim.ladder))
        main_sim.print_progress_bar(main_sim.num_games - battle_queue.qsize(), start_time)
        battle_queue.task_done()
