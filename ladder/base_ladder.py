"""Base Class for ladders to inherit from."""
from copy import deepcopy

from numpy.random import randint, shuffle
from ladder.elo import elo


class BaseLadder:
    """The class for the ladder."""

    def __init__(self, game=None, K_in=32):
        """
        Initialize a ladder for a specific game.

        :param game: GameEngine
            Game to be played on this ladder
        :param K_in: int
            K value to be used for calculating elo changes
            on this ladder
        """
        self.player_pool = []
        self.game_engine = game
        self.num_turns = 0
        self.k_value = K_in

    def add_player(self, player):
        """
        Add a player to the waiting pool.

        :param player: BaseAgent
            Player to be added to the ladder pool
        """
        # Check that player is not already in the pool
        for player_, _ in self.player_pool:
            if player_.id == player.id:
                raise ValueError("Player already in pool")

        # Add the player to the pool
        self.player_pool.append((
            player,
            self.num_turns
        ))
        shuffle(self.player_pool)

    def get_players(self, sort=False):
        """
        Return the players currently in the pool.

        :param sort: bool
            Whether or not to sort the output by elo
        """
        output = []
        for player, _ in self.player_pool:
            output.append(player)

        if sort:
            output = sorted(output,
                            key=lambda player: player.elo, reverse=True)
        return output

    def match_players(self):
        """Return a pair of players to play."""
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

        self.num_turns += 1
        return (player, opponent)

    def match_func(self, player1, player2_pair):
        """IMPLEMENT IN CHILD CLASS."""
        raise NotImplementedError("Implement in child class")

    def run_game(self):
        """Match players and run a game."""
        player, opp = self.match_players()
        player_copy = deepcopy(player)
        opp_copy = deepcopy(opp)

        outcome = self.game_engine.run(player, opp)

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

        :param winner: BaseAgent
            Player who won
        :param loser: BaseAgent
            Player who lost
        """
        new_winner_elo = elo(winner, loser, 1, self.k_value)
        new_loser_elo = elo(loser, winner, 0, self.k_value)
        winner.elo = new_winner_elo
        winner.num_wins += 1
        loser.elo = new_loser_elo
        loser.num_losses += 1
