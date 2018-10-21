"""Script for running Pokemon Simulation."""

from threading import Thread
from queue import Queue
from time import time

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from battle_engine.pokemon_engine import PokemonEngine
from file_manager.log_writer import LogWriter
from file_manager.team_reader import TeamReader
from simulation.base_type_logging_simulation import BaseLoggingSimulation
from simulation.base_simulation import load_config
from stats.calc import calculate_avg_elo


class PokemonSimulation(BaseLoggingSimulation):
    """Class for Pokemon Simulation."""

    def __init__(self, **kwargs):
        """Initialize this simulation."""
        pkmn_kwargs = kwargs
        pkmn_kwargs["game"] = PokemonEngine()
        pkmn_kwargs["prefix"] = "PKMN"

        self.config = load_config(kwargs["config"])
        self.type_log_writer = None
        self.data_delay = kwargs["data_delay"]
        self.multithread = kwargs.get("multithread", False)
        super().__init__(pkmn_kwargs)

    def add_agents(self):
        """Add the agents to this model."""
        for conf in self.config:
            conf_tr = TeamReader(prefix=conf["team_file"])
            conf_tr.process_files()
            conf_team = conf_tr.teams[0]
            for _ in range(int(self.num_players * conf["proportion"])):
                pkmn_agent = None
                if conf["agent_class"] == "basic":
                    pkmn_agent = PokemonAgent(
                        team=conf_team
                    )
                    pkmn_agent.type = conf["agent_type"]

                elif conf["agent_class"] == "basicplanning":
                    pkmn_agent = BasicPlanningPokemonAgent(
                        tier=conf["agent_tier"],
                        team=conf_team
                    )
                    pkmn_agent.type = conf["agent_type"]

                else:
                    raise RuntimeError("Invalid agent_class: {}".format(conf["agent_class"]))

                self.ladder.add_player(pkmn_agent)

    def init_type_log_writer(self):
        """Initialize Type Average Elo LogWriter."""
        header = []
        for conf in self.config:
            header.append(conf["agent_type"])

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
