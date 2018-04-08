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

    def run_turn(self, player1_move, player1, player2):
        """Run a turn of this battle."""
        player2_move = player2.make_move()
        turn_info = self.calculate_turn(player1_move, player2_move)

        player1.new_info(turn_info, "player1")
        player2.new_info(turn_info, "player2")

        # Figure out who faints at the end of this turn.
        if self.game_state["player1"]["active"].current_hp < 0:
            self.game_state["player1"]["active"] = None
        if self.game_state["player2"]["active"].current_hp < 0:
            self.game_state["player2"]["active"] = None

        self.update_gamestates(player1, player2)

        # If battle is not over, switch in next pokemon.
        outcome = self.win_condition_met()
        if not outcome["finished"]:
            update = False
            if self.game_state["player1"]["active"] is None:
                switchin_ind = player1.switch_faint()
                self.game_state["player1"]["active"] = \
                    self.game_state["player1"]["team"].pop(switchin_ind)
                update = True

            if self.game_state["player2"]["active"] is None:
                switchin_ind = player2.switch_faint()
                self.game_state["player2"]["active"] = \
                    self.game_state["player2"]["team"].pop(switchin_ind)
                update = True

            if update:
                self.update_gamestates(player1, player2)

        return turn_info, outcome
