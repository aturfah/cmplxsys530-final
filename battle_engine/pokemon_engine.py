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

    def run(self, player1, player2):
        """
        Run a game of pokemon.

        :param player1/2: PokemonAgent
            Players 1 and 2 for this game.
        """
        self.reset_game_state()
        self.initialize_battle(player1, player2)

        # Initial setting of outcome variable
        outcome = self.win_condition_met()
        while not outcome["finished"]:
            # Increment turn counter
            self.game_state["num_turns"] += 1

            # Each player makes a move
            player1_move = player1.make_move()
            player2_move = player2.make_move()

            outcome = self.run_single_turn(player1_move, player2_move, player1, player2)[0]

        if outcome["draw"]:
            # It was a draw, decide randomly
            return int(uniform() < 0.5)

        return outcome["winner"]

    def run_single_turn(self, player1_move, player2_move, player1, player2):
        """Run the turn for these moves."""
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

        return outcome, turn_info

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

        turn_info = []

        if not p1_switch and not p2_switch:
            turn_info = self.turn_both_attack(move1, move2)
        elif p1_switch:
            self.switch_pokemon("player1", move1[1])
            attack = self.game_state["player2"]["active"].moves[move2[1]]
            turn_info = self.attack("player2", attack)
        elif p2_switch:
            self.switch_pokemon("player2", move2[1])
            attack = self.game_state["player1"]["active"].moves[move1[1]]
            turn_info = self.attack("player1", attack)
        else:
            self.switch_pokemon("player1", move1[1])
            self.switch_pokemon("player2", move2[1])

        return turn_info

    def switch_pokemon(self, player, position):
        """
        Switch a player's pokemon out.

        :param player: str
            The player ("player1" or "player2") who is
            doing the switching.
        :param position: int
            The position in the team that this player
            is switching out to.
        """
        cur_active = self.game_state[player]["active"]
        self.game_state[player]["team"].append(cur_active)
        new_active = self.game_state[player]["team"].pop(position)
        self.game_state[player]["active"] = new_active

    def attack(self, attacker, move):
        """
        Attack opposing pokemon with the move.

        :param player: str
            The player ("player1" or "player2")
            who is attacking.
        :param move: dict
            The data for the move that is being done.
        """
        if attacker == "player1":
            defender = "player2"
        else:
            defender = "player1"

        atk_poke = self.game_state[attacker]["active"]
        def_poke = self.game_state[defender]["active"]

        # Do Damage
        damage = calculate_damage(move, atk_poke, def_poke)        
        def_poke.current_hp -= damage

        # Move boosts
        if "boosts" in move:
            if move["target"] == "self":
                for stat in move["boosts"]:
                    atk_poke.boosts[stat] += move["boosts"][stat]
                    atk_poke.boosts[stat] = min(atk_poke.boosts[stat], 6)
            else:
                for stat in move["boosts"]:
                    def_poke.boosts[stat] += move["boosts"][stat]
                    def_poke.boosts[stat] = min(def_poke.boosts[stat], 6)

        results = {}
        results["move"] = move
        results["damage"] = damage
        results["pct_damage"] = 100*damage/def_poke.max_hp
        results["attacker"] = attacker
        results["defender"] = defender
        results["atk_poke"] = atk_poke.name
        results["def_poke"] = def_poke.name
        return [results]

    def turn_both_attack(self, move1, move2):
        """
        Run a turn where both players attack.

        :param move1/2: dict
            The data for player1/2's moves.
        """
        move_dict = {}
        p1_active = self.game_state["player1"]["active"]
        p2_active = self.game_state["player2"]["active"]

        p1_move = p1_active.moves[move1[1]]
        p2_move = p2_active.moves[move2[1]]

        move_dict["player1"] = p1_move
        move_dict["player2"] = p2_move

        faster_player, slower_player = self.turn_order(p1_move, p2_move)

        # Faster pokemon attacks first.
        # If the slower pokemon is still alive,
        # it attacks as well.
        results = []
        new_data = self.attack(faster_player, move_dict[faster_player])
        results.extend(new_data)
        if self.game_state[slower_player]["active"].current_hp > 0:
            new_data = self.attack(slower_player, move_dict[slower_player])
            results.extend(new_data)

        return results

    def win_condition_met(self):
        """
        Determine whether or not condition for victory is met.

        Either all of one player's pokemon have fainted (in which
        case it is a victory), or maximum number of turns allowed
        have passed.
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

    def anonymize_gamestate(self, player_id):
        """
        Anonymize the internal gamestate for consumption by opponent.

        :param player_id: str
            The player whose data needs to be anonymized.
            Either "player1" or "player2"
        """
        data = deepcopy(self.game_state[player_id])
        return anonymize_gamestate_helper(data)

    def turn_order(self, p1_move, p2_move):
        """
        Calculate turn order for when players move.

        :param p1_move: Pokemon
            Player1's move.
        :param p2_active: Pokemon
            Player2's move.
        """
        if p1_move["priority"] != p2_move["priority"]:
            if p1_move["priority"] > p2_move["priority"]:
                faster_player = "player1"
                slower_player = "player2"
            else:
                faster_player = "player2"
                slower_player = "player1"
        else:
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

        return faster_player, slower_player

    def update_gamestates(self, player1, player2):
        """Update the player's gamestates to reflect the engine's gamestate."""
        player1.update_gamestate(
            self.game_state["player1"], self.anonymize_gamestate("player2"))
        player2.update_gamestate(
            self.game_state["player2"], self.anonymize_gamestate("player1"))


def anonymize_gamestate_helper(data):
    """Anonymize some gamestate data."""
    anon_data = {}

    anon_data["team"] = []
    for pokemon in data["team"]:
        pct_hp = pokemon.current_hp/pokemon.max_hp
        name = pokemon.name
        anon_data["team"].append({
            "name": name,
            "pct_hp": pct_hp
        })

    if data["active"] is not None:
        anon_data["active"] = {
            "name": data["active"].name,
            "pct_hp": data["active"].current_hp/data["active"].max_hp,
            "boosts": data["active"].boosts
        }
    else:
        anon_data["active"] = None

    return anon_data


def calculate_damage(move, attacker, defender):
    """
    Calculate damage of a move.

    :param move: dict
        Data of the attacking move.
    :param attacker: dict or Pokemon
        Data of the attacking Pokemon. Must support the [] operator.
    :param defender: dict or Pokemon
        Data of the defending Pokemon. Must support the [] operator.
    """
    # Calculate actual damage
    damage = floor(2*attacker["level"]/5 + 2)
    damage = damage * move["basePower"]
    if move["category"] == "Physical":
        damage = floor(damage * attacker.effective_stat("atk"))/defender.effective_stat("def")
    elif move["category"] == "Special":
        damage = floor(damage * attacker.effective_stat("spa"))/defender.effective_stat("spd")
    damage = floor(damage/50) + 2

    modifier = calculate_modifier(move, attacker, defender)
    # Critical Hit
    if uniform() < 0.0625:
        modifier = modifier * 1.5
    # Random Damage range
    modifier = modifier * uniform(0.85, 1.00)
    damage = floor(damage*modifier)

    return damage


def calculate_modifier(move, attacker, defender):
    """Calculate the damage modifier for an attack."""
    modifier = 1

    # STAB Modifier
    if move["type"] in attacker["types"]:
        modifier = modifier * 1.5

    # Weakness modifier
    for def_type in defender["types"]:
        if move["type"] in WEAKNESS_CHART[def_type]:
            modifier = modifier * WEAKNESS_CHART[def_type][move["type"]]

    return modifier
