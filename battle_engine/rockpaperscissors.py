"""Engine implementation for Rock, Paper, Scissors."""
from random import random

from agent.counter_rps_agent import CounterRPSAgent
from agent.adjusting_rps_agent import AdjustingRPSAgent

class RPSEngine:
    """Engine to run a game of rock, paper, scissors."""

    def __init__(self, num_games=1):
        """
        Init method for this class.

        Args:
            num_games (int): Number of games to play (Default 1).

        """
        if num_games % 2 == 0:
            raise AttributeError("num_games must be odd.")
        if num_games <= 0:
            raise AttributeError("num_games must be positive.")

        self.num_games = num_games
        self.reset_game_state()

    def reset_game_state(self):
        """
        Reset game state to all zeros.

        "0" corresponds to ties.
        "1" corresponds to player1 wins.
        "2" corresponds to player2 wins.

        """
        self.game_state = {}
        self.game_state[0] = 0
        self.game_state[1] = 0
        self.game_state[2] = 0

    def run(self, player1, player2):
        """
        Run <self.num_games> games.

        Returns 1 if player1 wins, 0 if player2 wins.
        In the case of a draw, flip a coin.

        :param player1: BaseAgent
            A player in this simulation.
        :param player2: BaseAgent
            The other player in this simulation.
        """
        self.reset_game_state()

        for player in [player1, player2]:
            if isinstance(player, CounterRPSAgent):
                player.reset_state()
            elif isinstance(player, AdjustingRPSAgent):
                player.reset_state()

        outcome = None
        for _ in range(self.num_games):
            p1_move = player1.make_move()
            p2_move = player2.make_move()

            if isinstance(player1, CounterRPSAgent):
                player1.update_info(last_move=p2_move)
            elif isinstance(player1, AdjustingRPSAgent):
                player1.update_info(opp_move=p2_move)

            if isinstance(player2, CounterRPSAgent):
                player2.update_info(last_move=p1_move)
            elif isinstance(player2, AdjustingRPSAgent):
                player2.update_info(opp_move=p1_move)

            results = rps_logic(p1_move, p2_move)
            self.game_state[results] += 1

            outcome = self.win_condition_met()
            if not outcome["draw"]:
                break

        if outcome["draw"]:
            # It was a draw, decide randomly
            return int(random() < 0.5)

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


def rps_logic(p1_move, p2_move):
    """
    Execute logic of RPS Game.

    Rock < Paper < Scissors < Rock
    """
    if p1_move == p2_move:
        # Same move, its a draw
        return 0
    elif (p1_move - p2_move) == 1 or (p1_move - p2_move) == -2:
        # Player1 wins (Paper vs Rock or Scissors vs Paper or Rock vs Scissors)
        return 1

    # Player2 wins
    return 2
