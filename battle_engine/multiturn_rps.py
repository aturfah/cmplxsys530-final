"""Engine for Best N/M RPS."""

import numpy as np
from agent.counter_rps_agent import CounterRPSAgent
from battle_engine.rockpaperscissors import RPSEngine


class MTRPSEngine(RPSEngine):
    """Multiturn RPS Engine class."""

    def __init__(self, num_games=3):
        """
        Initialize empty game_state.

        :param num_games: int
            Number of games to play.
        """
        if num_games % 2 == 0:
            raise AttributeError("num_games must be odd.")
        if num_games <= 0:
            raise AttributeError("num_games must be positive.")

        self.num_games = num_games
        self.reset_game_state()
        super().__init__()

    def reset_game_state(self):
        """Reset game state to all zeros."""
        self.game_state = {}
        self.game_state[0] = 0
        self.game_state[1] = 0
        self.game_state[2] = 0

    def run(self, player1, player2):
        """
        Run a set of games.

        Returns 1 if player1 wins, 0 if player2 wins.
        In the case of a draw, flip a coin.

        :param player1: BaseAgent
            A player in this simulation.
        :param player2: BaseAgent
            The other player in this simulation.
        """
        self.reset_game_state()

        if isinstance(player1, CounterRPSAgent):
            player1.reset_state()
        if isinstance(player2, CounterRPSAgent):
            player2.reset_state()

        outcome = None
        for _ in range(self.num_games):
            p1_move = player1.make_move()
            p2_move = player2.make_move()

            if isinstance(player1, CounterRPSAgent):
                player1.last_move = p2_move
            if isinstance(player2, CounterRPSAgent):
                player2.last_move = p1_move

            results = self.rps_logic(p1_move, p2_move)
            self.game_state[results] += 1

            outcome = self.win_condition_met()
            if not outcome["draw"]:
                break

        if outcome["draw"]:
            # It was a draw, decide randomly
            return int(np.random.uniform() < 0.5)

        return outcome["winner"]

    def win_condition_met(self):
        """
        Assess whether or not condition for winning met and return winner.

        If number of games necessary for victory met, return the winner.
        """
        p1_wins = self.game_state[1]
        p2_wins = self.game_state[2]
        wins_needed = int(self.num_games/2)+1

        # Initialize results
        result = {}
        result["draw"] = True
        result["winner"] = None

        if p1_wins >= wins_needed:
            result["draw"] = False
            result["winner"] = 1
        elif p2_wins >= wins_needed:
            result["draw"] = False
            result["winner"] = 0

        return result
