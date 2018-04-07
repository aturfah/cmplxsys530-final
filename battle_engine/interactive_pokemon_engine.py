"""Pokemon Engine for the player to play against."""

from copy import deepcopy

from battle_engine.pokemon_engine import PokemonEngine

class InteractivePokemonEngine(PokemonEngine):
    """The class itself."""

    def run(self, player1, player2):
        """Discontinued feature, see run_turn."""
        raise NotImplementedError("Not implemented in this subclass. See run_turn()")

    def initialize_battle(self, player1, player2):
        """Initialize this battle and set the players' gamestates."""
        # Initialize the players' teams
        self.game_state["player1"]["team"] = deepcopy(player1.team)
        self.game_state["player2"]["team"] = deepcopy(player2.team)

        # Each player leads with first pokemon on their side
        self.game_state["player1"]["active"] = \
            self.game_state["player1"]["team"].pop(0)
        self.game_state["player2"]["active"] = \
            self.game_state["player2"]["team"].pop(0)

        # Set initial game states for players
        player1.update_gamestate(
            self.game_state["player1"], self.anonymize_gamestate("player2"))
        player2.update_gamestate(
            self.game_state["player2"], self.anonymize_gamestate("player1"))

        player1.init_opp_gamestate(self.game_state["player2"]["team"],
                                   self.game_state["player2"]["active"])
        player2.init_opp_gamestate(self.game_state["player1"]["team"],
                                   self.game_state["player1"]["active"])

    def run_turn(self, player_move, player2):
        """Run a turn of this battle."""
        pass
