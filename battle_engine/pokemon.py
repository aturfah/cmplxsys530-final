"""Engine to run the turn of a pokemon game."""

from math import floor
from copy import deepcopy

from numpy.random import uniform

from config import WEAKNESS_CHART


class PokemonEngine():
    """Class to run a pokemon game."""

    def __init__(self, generation="gen7", turn_limit=2000):
        """Initialize a new PokemonEngine."""
        self.generation = generation
        self.turn_limit = turn_limit
        self.reset_game_state()

    def reset_game_state(self):
        """Reset game states for a new game."""
        self.game_state = {}
        self.game_state["player1"] = {}
        self.game_state["player1"]["active"] = None
        self.game_state["player1"]["team"] = None
        self.game_state["player2"] = {}
        self.game_state["player2"]["active"] = None
        self.game_state["player2"]["team"] = None
        self.game_state["num_turns"] = 0

    def run(self, player1, player2):
        """Run a game of pokemon."""
        print("##### BEGIN #####\n")
        self.reset_game_state()

        # Initialize the players' teams
        self.game_state["player1"]["team"] = deepcopy(player1.team)
        self.game_state["player2"]["team"] = deepcopy(player2.team)

        # Each player leads with first pokemon on their side
        self.game_state["player1"]["active"] = \
            self.game_state["player1"]["team"].pop(0)
        self.game_state["player2"]["active"] = \
            self.game_state["player2"]["team"].pop(0)

        player1.update_gamestate(self.game_state["player1"])
        player2.update_gamestate(self.game_state["player2"])

        outcome = self.win_condition_met()
        while not outcome["finished"]:
            # Increment turn counter
            self.game_state["num_turns"] += 1

            # Each player makes a move
            player1_move = player1.make_move()
            player2_move = player2.make_move()
            self.calculate_turn(player1_move, player2_move)

            # Update their gamestates
            player1.update_gamestate(self.game_state["player1"])
            player2.update_gamestate(self.game_state["player2"])

            outcome = self.win_condition_met()
            if not outcome["finished"]:
                update = False
                if self.game_state["player1"]["active"] is None:
                    switchin_ind = player1.switch_faint()
                    self.game_state["player1"]["active"] = \
                        self.game_state["player1"]["team"].pop(switchin_ind)
                    update = True
                    new_active = self.game_state["player1"]["active"]
                    print("{} sent out {} ({}/{})"
                          .format("player1",
                                  new_active.name,
                                  new_active.current_hp,
                                  new_active.max_hp))

                if self.game_state["player2"]["active"] is None:
                    switchin_ind = player2.switch_faint()
                    self.game_state["player2"]["active"] = \
                        self.game_state["player2"]["team"].pop(switchin_ind)
                    new_active = self.game_state["player2"]["active"]
                    print("{} sent out {} ({}/{})"
                          .format("player2",
                                  new_active.name,
                                  new_active.current_hp,
                                  new_active.max_hp))
                    update = True
                if update:
                    player1.update_gamestate(self.game_state["player1"])
                    player2.update_gamestate(self.game_state["player2"])

            print(" ")

        print("##### FINISHED #####\n")
        if outcome["draw"]:
            # It was a draw, decide randomly
            return int(uniform() < 0.5)

        return outcome["winner"]

    def calculate_turn(self, move1, move2):
        """
        Calculate results of a turn of a pokemon game.

        :param move1/move2: tuple
            Player 1/2's move respectively. Tuple of size 2. First
            value is the type of move (either SWITCH or ATTACK),
            followed by the index of the attack or pokemon to be
            switched to.
        """
        p1_switch = move1[0] == "SWITCH"
        p2_switch = move2[0] == "SWITCH"

        if not p1_switch and not p2_switch:
            # Both attack
            self.turn_both_attack(move1, move2)
        elif p1_switch:
            # player1 switches, player2 attacks
            self.switch_pokemon("player1", move1[1])
            self.turn_one_attack("player2", move2)
        elif p2_switch:
            # player2 switches, player1 attacks
            self.switch_pokemon("player2", move2[1])
            self.turn_one_attack("player1", move1)
        else:
            # Both switch
            self.switch_pokemon("player1", move1[1])
            self.switch_pokemon("player2", move2[1])

    def switch_pokemon(self, player, position):
        """Switch a player's pokemon out."""
        cur_active = self.game_state[player]["active"]
        self.game_state[player]["team"].append(cur_active)
        new_active = self.game_state[player]["team"].pop(position)
        self.game_state[player]["active"] = new_active
        print("{} switched to {} ({}/{})"
              .format(player,
                      new_active.name,
                      new_active.current_hp,
                      new_active.max_hp))

    def turn_one_attack(self, attacker, move):
        """Turn where only one player attacks."""
        if attacker == "player1":
            defender = "player2"
        else:
            defender = "player1"

        atk_poke = self.game_state[attacker]["active"]
        def_poke = self.game_state[defender]["active"]

        atk_move = atk_poke.moves[move[1]]

        def_poke.current_hp -= calculate_damage(atk_move, atk_poke, def_poke)
        if def_poke.current_hp < 0:
            def_poke = None

        self.game_state[defender]["active"] = def_poke
        print("{} attacked with {}".format(attacker, atk_move["name"]))

    def turn_both_attack(self, move1, move2):
        """Run a turn where both players attack."""
        move_dict = {}
        p1_active = self.game_state["player1"]["active"]
        p2_active = self.game_state["player2"]["active"]

        move_dict["player1"] = p1_active.moves[move1[1]]
        move_dict["player2"] = p2_active.moves[move2[1]]

        # Decide who goes first
        p1_speed = p1_active.speed
        p2_speed = p2_active.speed

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

        faster_poke = self.game_state[faster_player]["active"]
        slower_poke = self.game_state[slower_player]["active"]

        # Do the move
        slower_poke.current_hp -= calculate_damage(
            move_dict[faster_player], faster_poke, slower_poke)
        print("{}'s {} attacked with {}"
              .format(faster_player,
                      faster_poke.name,
                      move_dict[faster_player]["name"]))
        if slower_poke.current_hp > 0:
            faster_poke.current_hp -= calculate_damage(
                move_dict[slower_player], slower_poke, faster_poke)
            print("{}'s {} attacked with {}"
                  .format(slower_player,
                          slower_poke.name,
                          move_dict[slower_player]["name"]))

        if slower_poke.current_hp < 0:
            print("{} fainted...".format(slower_poke.name))
            slower_poke = None
        if faster_poke.current_hp < 0:
            print("{} fainted...".format(faster_poke.name))
            faster_poke = None

        # Update the game state
        self.game_state[faster_player]["active"] = faster_poke
        self.game_state[slower_player]["active"] = slower_poke

    def win_condition_met(self):
        """
        Determine whether or not condition for victory is met.

        Either all of one player's pokemon have fainted
        """
        p1_state = self.game_state["player1"]
        p2_state = self.game_state["player2"]

        too_many_turns = self.game_state["num_turns"] > self.turn_limit

        p1_lost = p1_state["active"] is None and not p1_state["team"]
        p1_lost = p1_lost or too_many_turns
        p2_lost = p2_state["active"] is None and not p2_state["team"]
        p2_lost = p2_lost or too_many_turns

        result = {}
        result["finished"] = False
        result["winner"] = None

        if not p1_lost and not p2_lost:
            # Not finished
            pass
        elif p1_lost and not p2_lost:
            # Player1 lost
            result["finished"] = True
            result["draw"] = False
            result["winner"] = 0
        elif p2_lost and not p1_lost:
            # Player2 lost
            result["finished"] = True
            result["draw"] = False
            result["winner"] = 1
        else:
            # Both players lost, like a final
            # Pokemon explosion or something.
            result["finished"] = True
            result["draw"] = True
            result["winner"] = None

        return result


def calculate_damage(move, attacker, defender):
    """Calculate damage of a move."""
    # Calculate actual damage
    damage = floor(2*attacker.level/5 + 2)
    damage = damage * move["basePower"]
    if move["category"] == "Physical":
        damage = floor(damage * attacker.attack)/defender.defense
    elif move["category"] == "Special":
        damage = floor(damage * attacker.sp_attack)/defender.sp_defense
    damage = floor(damage/50) + 2

    # Random modifier
    modifier = uniform(0.85, 1.00)

    # STAB Modifier
    if move["type"] in attacker.types:
        modifier = modifier * 1.5

    # Weakness modifier
    for def_type in defender.types:
        if move["type"] in WEAKNESS_CHART[def_type]:
            modifier = modifier * WEAKNESS_CHART[def_type][move["type"]]

    damage = floor(damage*modifier)

    return damage
