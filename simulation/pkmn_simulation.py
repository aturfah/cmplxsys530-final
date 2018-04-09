"""Script for running Pokemon Simulation."""

from threading import Thread, Lock
from queue import Queue

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
        self.multithread = kwargs.get("multithread", True)
        super().__init__(pkmn_kwargs)

    def add_agents(self):
        """Add the agents to this model."""
        for ind in range(self.num_players):
            if ind % 3 == 1:
                pkmn_agent = PokemonAgent(default_team_floatzel())
                pkmn_agent.type = "random.floatzel"
            elif ind % 3 == 2:
                pkmn_agent = PokemonAgent(default_team_ivysaur())
                pkmn_agent.type = "random.ivysaur"
            else:
                pkmn_agent = PokemonAgent(default_team_spinda())
                pkmn_agent.type = "random.spinda"

            self.ladder.add_player(pkmn_agent)

        for ind in range(self.num_players):
            if ind % 3 == 1:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_floatzel())
                pkmn_agent.type = "planning.floatzel"
            elif ind % 3 == 2:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_ivysaur())
                pkmn_agent.type = "planning.ivysaur"
            else:
                pkmn_agent = BasicPlanningPokemonAgent(
                    tier="pu", team=default_team_spinda())
                pkmn_agent.type = "planning.spinda"
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

        thread_lock = Lock()

        for _ in range(4):
            battle_thread = Thread(target=battle, args=(self.ladder,
                                                        battle_queue,
                                                        battle_results_queue,
                                                        type_results_queue,
                                                        self.data_delay,
                                                        thread_lock))
            battle_thread.start()

        while not battle_results_queue.empty():
            output, player1, player2 = battle_results_queue.get()
            self.write_player_log(output, player1, player2)

        while not type_results_queue.empty():
            data_line = type_results_queue.get()
            self.type_log_writer.write_line(data_line)


def battle(ladder, battle_queue, output_queue, type_queue, data_delay, thread_lock):
    """Simulation code for a thread to run."""
    while not battle_queue.empty():
        battle_queue.get()
        results = ladder.run_game(thread_lock)
        output_queue.put(results)
        print("\r{}   \r".format(battle_queue.qsize()), end="")
        battle_queue.task_done()
        if battle_queue.qsize() % data_delay == 0:
            print("CALCULATING GROUP ELO", battle_queue.qsize())
            type_queue.put(calculate_avg_elo(ladder))
