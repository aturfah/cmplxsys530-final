"""Pokemon agent who's moves are determined by maximizing personal gain."""

from agent.basic_pokemon_agent import PokemonAgent

from config import USAGE_STATS

class BasicPlanningPokemonAgent(PokemonAgent):
    """
    Class for PokemonAgent who calculates the next move by maximizing some function.

    This agent will maximize the game_position given the opponent's moves are all
    equally likely.
    """
    def __init__(self, tier, **kwargs):
        """Initialize a player with a specific tier."""
        super().__init__(*kwargs)
        self.tier = tier

    def make_move(self):
        """Choose the move to make."""
        player_opts, opp_opts = self.generate_possibilities()

    def generate_possibilities(self):
        """Generate a two lists of possible player and opponent moves."""
        player_opts = []
        opp_opts = []

        # My possible attacks
        posn = 0
        for _ in self.gamestate["active"].moves:
            player_opts.append(("ATTACK", posn))
            posn += 1

        # My possible switches
        posn = 0
        for _ in self.gamestate["team"]:
            player_opts.append(("SWITCH", posn))
            posn += 1

        # Opponent's possible attacks
        posn = 0
        opp_active_poke = self.opp_gamestate["data"]["active"]["name"]
        opp_moves = []
        if opp_active_poke in self.opp_gamestate["moves"]:
            for move in self.opp_gamestate["moves"][opp_active_poke]:
                opp_moves.append(move)
        if len(opp_moves) < 4:
            print(USAGE_STATS[self.tier][opp_active_poke])

        # Opponent's possible switches
        posn = 0
        for poke in self.opp_gamestate["data"]["team"]:
            poke_name = poke["name"]


        return player_opts, opp_opts
