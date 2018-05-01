"""Base Class for ladders to inherit from."""
from copy import deepcopy
from threading import Lock

from numpy.random import randint
from ladder.elo import elo


class BaseLadder:
    """
    The class for the ladder.

    Attributes:
        player_pool (list): List of players in the pool.
        game_engine (battle_engine): Engine to run the game.
        num_turns (int): Number of games that have been played.
        k_value (int): K value to be used for calculating elo changes
            on this ladder.
        thread_lock (Lock): Lock used in multithreaded simulations.

    """

    def __init__(self, game=None, K_in=32):
        """
        Initialize a ladder for a specific game.

        Args:
            game (battle_engine): Game to be played on this ladder.
            K_in (int): K value to be used for calculating elo changes
                on this ladder.

        """
        self.player_pool = []
        self.game_engine = game
        self.num_turns = 0
        self.k_value = K_in
        self.thread_lock = Lock()

    def add_player(self, player):
        """
        Add a player to the waiting pool.

        Args:
            player (BaseAgent): Player to be added to the ladder pool

        """
        self.thread_lock.acquire()

        # Check that player is not already in the pool
        for player_, _ in self.player_pool:
            if player_.id == player.id:
                raise ValueError("Player already in pool")

        # Add the player to the pool
        self.player_pool.append((
            player,
            self.num_turns
        ))

        self.thread_lock.release()

    def get_players(self, sort=False):
        """
        Return the players currently in the pool.

        Args:
            sort (bool): Whether or not to sort the output by Elo raking.

        Returns:
            List of players, either sorted or not sorted.

        """
        output = []
        self.thread_lock.acquire()
        for player, _ in self.player_pool:
            output.append(player)
        self.thread_lock.release()

        if sort:
            output = sorted(output,
                            key=lambda player: player.elo, reverse=True)
        return output

    def match_players(self):
        """
        Return a pair of players to play.

        Returns:
            A pair of players matched by the ladder's match_func.

        """
        self.thread_lock.acquire()

        # Select a random player
        player_ind = randint(low=0, high=len(self.player_pool))
        player = self.player_pool[player_ind][0]
        del self.player_pool[player_ind]

        # Select that player's opponent (based on weighting function)
        # candidate_opponents = sorted(self.player_pool,
        #                        key=lambda val: self.match_func(player, val),
        #                        reverse=True)[:min(5, len(self.player_pool))]

        # opponent_index = randint(len(candidate_opponents))
        # opponent_pair = candidate_opponents[opponent_index]
        opponent_pair = sorted(self.player_pool,
                               key=lambda val: self.match_func(player, val),
                               reverse=True)[0]
        opponent = opponent_pair[0]
        opponent_ind = self.player_pool.index(opponent_pair)
        del self.player_pool[opponent_ind]

        self.thread_lock.release()

        self.num_turns += 1
        return (player, opponent)

    def match_func(self, player1, player2_pair):
        """IMPLEMENT IN CHILD CLASS."""
        raise NotImplementedError("Implement in child class")

    def run_game(self):
        """
        Match players and run a game.

        Returns:
            Tuple with the winner of the game, as well as data on the
                players involved in the game.

        """
        player, opp = self.match_players()
        player_copy = deepcopy(player)
        opp_copy = deepcopy(opp)

        # Make a copy to be thread safe(?)
        temp_engine = deepcopy(self.game_engine)
        outcome = temp_engine.run(player, opp)

        if outcome == 1:
            self.update_players(player, opp)
        else:
            self.update_players(opp, player)

        self.add_player(player)
        self.add_player(opp)

        return (outcome, player_copy, opp_copy)

    def update_players(self, winner, loser):
        """
        Update values for winner and loser.

        Args:
            winner (BaseAgent): The player who won.
            loser (BaseAgent): The player who lost.

        """
        new_winner_elo = elo(winner, loser, 1, self.k_value)
        new_loser_elo = elo(loser, winner, 0, self.k_value)
        winner.elo = new_winner_elo
        winner.num_wins += 1
        loser.elo = new_loser_elo
        loser.num_losses += 1
