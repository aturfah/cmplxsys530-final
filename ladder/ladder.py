""" Methods for matching players together by elo ranking """

from numpy.random import randint


class Ladder:
    def __init__(self):
        """ Initialize a ladder """
        self.player_pool = []
        self.num_turns = 0

    def add_player(self, player):
        """ Add a player to the waiting pool """
        # Check that player is not already in the pool
        for player_, _ in self.player_pool:
            if player_.id == player.id:
                raise ValueError("Player already in pool")

        # Add the player to the pool
        self.player_pool.append((
            player,
            self.num_turns
        ))

    def match_players(self):
        """ Return a pair of players to play """
        # Select a random player
        player_ind = randint(low=0, high=len(self.player_pool))
        player = self.player_pool[player_ind][0]
        del self.player_pool[player_ind]

        # Select that player's opponent (for now its random)
        opponent_ind = randint(low=0, high=len(self.player_pool))
        opponent = self.player_pool[opponent_ind][0]
        del self.player_pool[opponent_ind]

        self.num_turns += 1
        return (player, opponent)
