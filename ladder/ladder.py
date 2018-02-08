"""Methods for matching players together by elo ranking."""

from numpy.random import randint
from ladder.elo import elo


class Ladder:
    """The class for the ladder."""

    def __init__(self, K_in=32):
        """Initialize a ladder."""
        self.player_pool = []
        self.num_turns = 0
        self.k_value = K_in

    def add_player(self, player):
        """Add a player to the waiting pool."""
        # Check that player is not already in the pool
        for player_, _ in self.player_pool:
            if player_.id == player.id:
                raise ValueError("Player already in pool")

        # Add the player to the pool
        self.player_pool.append((
            player,
            self.num_turns
        ))

    def get_players(self, sort=False):
        """Return the players currently in the pool."""
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

        # Select that player's opponent (based on waiting function)
        opponent_pair = sorted(self.player_pool,
                               key=lambda val: self.match_func(player, val),
                               reverse=True)[0]
        opponent = opponent_pair[0]
        opponent_ind = self.player_pool.index(opponent_pair)
        del self.player_pool[opponent_ind]

        self.num_turns += 1
        return (player, opponent)

    def match_func(self, player1, player2_pair):
        """
        Calculate the match score for two players.

        Players with similar elo rankings should be matched together.
        In addition, players who have been waiting for a long time should
        get to play sooner.

        Functional form is <Turns_waiting>/abs(<Difference in Elo scores>)

        :param player1: The player who is being matched
        :param player2: The candidate player/turns waiting pair
        """
        elo_factor = 1/max(abs(player1.elo - player2_pair[0].elo), 1)
        turn_factor = max((self.num_turns - player2_pair[1]), 1)

        return elo_factor*turn_factor

    def run_game(self, game_engine):
        """Match players and run a game."""
        player, opp = self.match_players()

        outcome = game_engine.run(player, opp)

        if outcome == 1:
            self.update_players(player, opp)
        else:
            self.update_players(opp, player)

        self.add_player(player)
        self.add_player(opp)

    def update_players(self, winner, loser):
        """Update values for winner and loser."""
        new_winner_elo = elo(winner, loser, 1, self.k_value)
        new_loser_elo = elo(loser, winner, 0, self.k_value)
        winner.elo = new_winner_elo
        winner.num_wins += 1
        loser.elo = new_loser_elo
        loser.num_losses += 1
