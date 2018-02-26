"""Engine to run the turn of a pokemon game."""

from numpy.random import uniform

from config import MOVE_DATA
from config import POKEMON_DATA


class PokemonEngine():
    """Class to run a pokemon game."""

    def __init__(self, generation="gen7", turn_limit=2000):
        """Initialization method."""
        self.generation = generation
        self.turn_limit = turn_limit
        self.reset_game_state()

    def reset_game_state(self):
        """Reset game states for a new game."""
        print("Resetting game states!")
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
        self.game_state["player1"]["active"] = \
            self.game_state["player1"]["team"].pop(0)
        self.game_state["player2"]["active"] = \
            self.game_state["player2"]["team"].pop(0)

        while not self.win_condition_met():
            print("Running moves!")
            # Each player makes a move
            player1_move = player1.make_move()
            player2_move = player2.make_move()
            self.calculate_turn(player1_move, player2_move)

            # Update their gamestates
            player1.update_gamestate(self.game_state["player1"])
            player2.update_gamestate(self.game_state["player2"])
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
        print("Player1's move: {}".format(move1))
        print("Player2's move: {}".format(move2))

        move_dict = {}
        move_dict["player1"] = move1
        move_dict["player2"] = move2

        # Decide who goes first
        p1_speed = self.game_state["player1"]["active"].speed
        p2_speed = self.game_state["player2"]["active"].speed

        if p1_speed == p2_speed:
            # Speed tie, coin flip
            if uniform() > 0.5:
                faster_player = "player1"
                slower_player = "player2"
            else:
                faster_player = "player2"
                slower_player = "player1"
        elif p1_speed > p2_speed:
            # Player1 goes first
            faster_player = "player1"
            slower_player = "player2"
        else:
            # Player2 goes first
            faster_player = "player2"
            slower_player = "player1"

        # Do the move
        faster_poke = self.game_state[faster_player]["active"]
        slower_poke = self.game_state[slower_player]["active"]
        slower_poke.current_hp -= calculate_damage(
            move_dict[faster_player], faster_poke, slower_poke)
        if slower_poke.current_hp > 0:
            faster_poke.current_hp -= calculate_damage(
                move_dict[slower_player], slower_poke, faster_poke)

        if slower_poke.current_hp < 0:
            slower_poke = None
        if faster_poke.current_hp < 0:
            faster_poke = None

        self.game_state[faster_player]["active"] = faster_poke
        self.game_state[slower_player]["active"] = slower_poke

    def win_condition_met(self):
        """
        Determine whether or not condition for victory is met.

        Either all of one player's pokemon have fainted
        """
        return False


def calculate_damage(move, attacker, defender):
    damage = 2*attacker.level/5 + 2
    damage = damage * move["basePower"]
    if move["category"] == "Physical":
        damage = damage * attacker.attack/defender.defense
    elif move["category"] == "Special":
        damage = damage * attacker.sp_attack/defender.sp_defense
    damage = damage/50 + 2

    modifier = uniform(0.85, 1.00)

    damage = damage*modifier

    return damage
