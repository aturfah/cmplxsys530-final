"""Pokemon agent who's moves are determined by maximizing personal gain."""

from agent.basic_pokemon_agent import PokemonAgent


class BasicPlanningPokemonAgent(PokemonAgent):
    """
    Class for PokemonAgent who calculates the next move by maximizing some function.

    This agent will maximize the game_position given the opponent's moves are all
    equally likely.
    """
    def make_move(self):
        """Choose the move to make."""
        player_opts, opp_opts = self.generate_possibilities()

    def generate_possibilities(self):
        """Generate a two lists of possible player and opponent moves."""
        player_opts = []
        opp_opts = []

        return player_opts, opp_opts
