"""Base Class for ladders to inherit from."""
from copy import deepcopy
from threading import Lock

from random import randint
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
        selection_size (int): Number of players to use as potential
            matches (before choosing randomly).
        thread_lock (Lock): Lock used in multithreaded simulations.

    """

    def __init__(self, game=None, K_in=32, selection_size=1):
        """
        Initialize a ladder for a specific game.

        Args:
            game (battle_engine): Game to be played on this ladder.
            K_in (int): K value to be used for calculating elo changes
                on this ladder.
            selection_size (int): Number of players to use as potential
            matches (before choosing randomly).

        """
        self.player_pool = []
        self.game_engine = game
        self.num_turns = 0
        self.k_value = K_in
        self.selection_size = selection_size
        self.thread_lock = Lock()

    def add_player(self, player):
        """
        Add a player to the waiting pool.

        Args:
            player (BaseAgent): Player to be added to the ladder pool

        """
        self.thread_lock.acquire()

        # Check that player is not already in the pool
        for player_tuple in self.player_pool:
            if player_tuple[0].id == player.id:
                player.in_game = False
                self.player_pool.remove(player_tuple)

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

        Raises:
            RuntimeError: If either no players in the pool or
                only a single player available.

        """
        self.thread_lock.acquire()

        available_players = self.available_players()

        # Check if no players ready
        if not available_players or len(available_players) == 1:
            self.thread_lock.release()
            raise RuntimeError("No players left in pool.")

        # Select a random player
        available_ind = randint(a=0, b=(len(available_players)-1))
        player = available_players[available_ind][0]
        del available_players[available_ind]
        player.in_game = True

        # Get that player's opponent
        candidate_opponents = self.get_candidate_matches(player, available_players)

        opponent_choice = randint(0, len(candidate_opponents)-1)
        opponent_pair = candidate_opponents[opponent_choice]
        opponent = opponent_pair[0]
        opponent.in_game = True

        self.thread_lock.release()

        self.num_turns += 1
        return (player, opponent)

    def get_candidate_matches(self, player, available_players=None):
        """
        Get the selection of players who are closest to <player>.

        Args:
            player (BaseAgent): Player for whom we are matching.
            match_pool (list): List of players from whom to choose.

        Returns:
            List of length self.selection_size of potential opponents.

        """
        # Select that player's opponent (based on weighting function)
        match_pool = None
        if available_players is None:
            match_pool = self.available_players()
        else:
            match_pool = available_players

        candidate_opponents = sorted(match_pool,
                                     key=lambda val: self.match_func(player, val),
                                     reverse=True)[:min(self.selection_size, len(match_pool))]

        return candidate_opponents

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
            self.update_player_stats(player, opp)
        else:
            self.update_player_stats(opp, player)

        self.add_player(player)
        self.add_player(opp)

        return (outcome, player_copy, opp_copy)

    def update_player_stats(self, winner, loser):
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

    def available_players(self):
        """Return list of players available to match."""
        available_players = []
        for player_tuple in self.player_pool:
            if not player_tuple[0].in_game:
                available_players.append(player_tuple)

        return available_players
