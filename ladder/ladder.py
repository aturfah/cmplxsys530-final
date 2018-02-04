""" Methods for matching players together by elo ranking """

from numpy.random import randint
from ladder.elo import elo


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

    def update_players(self, winner, loser):
        """ Update values for winner and loser """
        new_winner_elo = elo(winner, loser, 1)
        new_loser_elo = elo(winner, loser, 0)
        winner.elo = new_winner_elo
        winner.num_wins += 1
        loser.elo = new_loser_elo
        loser.num_losses += 1

    def run_game(self, game_engine):
        """ Match players and run a game """
        player, opp = self.match_players()

        outcome = game_engine.run(player, opp)

        if outcome == 1:
            self.update_players(player, opp)
        else:
            self.update_players(opp, player)

        add_player(player)
        add_player(opp)
