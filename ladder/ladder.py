""" Methods for matching players together by elo ranking """

from numpy.random import randint


class Ladder:
    def __init__(self):
        """ Initialize a ladder """
        self.player_pool = set()
        self.num_turns = 0

    def add_player(self, player):
        """ Add a player to the waiting pool """
        self.player_pool.add((
            player,
            self.num_turns
        ))

    def match():
        """ Return a pair of players to play """
        # Select a random player
        player_ind = randint(low=0, high=length(self.player_pool))
        player = player_pool[player_ind][0]
        del player_pool[player_ind]

        # Select that player's opponent (for now its random)
        opponent_ind = randint(low=0, high=length(self.player_pool))
        opponent = player_pool[opponent_ind][0]
        del player_pool[opponent_ind]

        self.num_turns += 1
        return (player, opponent)
