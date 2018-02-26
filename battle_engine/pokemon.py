"""Engine to run the turn of a pokemon game."""

from config import MOVE_DATA
from config import POKEMON_DATA

class PokemonEngine():
    """Class to run a pokemon game."""

    def __init__(self, generation, turn_limit=2000):
        """Initialization method."""
        self.generation = generation
        self.turn_limit = turn_limit
        self.reset_game_state()

    def reset_game_state(self):
        self.game_state = {}
        self.game_state["player1"] = {}
        self.game_state["player1"]["active"] = None
        self.game_state["player1"]["team"] = None
        self.game_state["player2"] = {}
        self.game_state["player2"]["active"] = None
        self.game_state["player2"]["team"] = None

    def run(self, player1, player2):
        """Run a game of pokemon."""
        self.reset_game_state()
        
        # Initialize the players' teams
        self.game_state["player1"]["team"] = player1.team
        self.game_state["player2"]["team"] = player2.team

        # Each player leads with first pokemon on their side
        self.game_state["player1"]["active"] = self.game_state["player1"]["team"].pop(0)
        self.game_state["player2"]["active"] = self.game_state["player2"]["team"].pop(0)


        while not self.win_condition_met():
            player1_move = player1.make_move()
            player2_move = player2.make_move()
            self.calculate_turn(player1_move, player2_move)
            break

        return 0

    def calculate_turn(self, move1, move2):
        """
        Calculate results of a turn of a pokemon game.

        :param move1/move2: tuple
            Player 1/2's move respectively. Tuple of size 2. First
            value is the type of move (either SWITCH or ATTACK),
            followed by the index of the attack or pokemon to be
            switched to.
        """
        


    def win_condition_met(self):
        """
        Determine whether or not condition for victory is met.

        Either all of one player's pokemon have fainted
        """
        return False
