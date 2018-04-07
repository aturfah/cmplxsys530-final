"""Pokemon Engine for the player to play against."""

from battle_engine.pokemon_engine import PokemonEngine

class InteractivePokemonEngine(PokemonEngine):
    """The class itself."""

    def run(self, player1, player2):
        """Discontinued feature, see run_turn."""
        raise NotImplementedError("Not implemented in this subclass. See run_turn()")

    def initialize_battle(self, player1, player2):
        """Initialize this battle and set the players' gamestates."""
        pass

    def run_turn(self, player_move, player2):
        """Run a turn of this battle."""
        pass
