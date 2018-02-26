"""Engine to run the turn of a pokemon game."""

class PokemonEngine():
    """Class to run a pokemon game."""
    def __init__(self, generation, turn_limit=2000):
        """Initialization method."""
        self.generation = generation
        self.turn_limit = turn_limit
        self.reset_game_state()

    def reset_game_state(self):
        self.game_state = {}
    
    def run(self, player1, player2):
        """Run a game of pokemon."""
        pass
        
    def calculate_turn(self, move1, move2):
        """
        Calculate results of a turn of a pokemon game.

        :param move1/move2: tuple
            Player 1/2's move respectively. Tuple of size 2. First
            value is the type of move (either SWITCH or ATTACK),
            followed by the index of the attack or pokemon to be
            switched to.
        """
        pass