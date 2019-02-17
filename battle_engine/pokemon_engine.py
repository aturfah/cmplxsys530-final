"""Engine to run the turn of a pokemon game."""

from math import floor
from copy import deepcopy
from uuid import uuid4

from random import random

from config import (PAR_STATUS, FRZ_STATUS, SLP_STATUS, TOX_STATUS)

from file_manager.log_writer import LogWriter
from pokemon_helpers.pokemon import default_boosts
from pokemon_helpers.calculate import calculate_status_damage


class PokemonEngine():
    """
    Class to run a pokemon game.

    Attributes:
        generation (str): Generation of Pokemon's mechanic to use.
        turn_limit (int): Maximum number of turns to play for.
        log_turn_flag (bool): Flag whether or not to log each game.

    """

    def __init__(self, generation="gen7", turn_limit=2000, log_turns=False):
        """Initialize a new PokemonEngine."""
        self.generation = generation
        self.turn_limit = turn_limit
        self.log_turn_flag = log_turns
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
        """
        Initialize this battle and set the players' gamestates.

        Args:
            player1 (PokemonAgent): Object corresponding to first player.
            player2 (PokemonAgent): object corresponding to second player.

        """
        # Reset internal gamestates
        player1.reset_gamestates()
        player2.reset_gamestates()

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

        Args:
            player1 (PokemonAgent): Object corresponding to first player.
            player2 (PokemonAgent): Object corresponding to second palyer.

        Returns:
            Boolean whether or not player1 won the game.

        """
        self.reset_game_state()
        self.initialize_battle(player1, player2)

        # Initialize Log Writer to write turn info
        turn_logwriter = None
        if self.log_turn_flag:
            turn_logwriter = init_player_logwriter(player1, player2)

        # Initial setting of outcome variable
        outcome = self.win_condition_met()
        while not outcome["finished"]:
            # Increment turn counter
            self.game_state["num_turns"] += 1

            # Each player makes a move
            player1_move = player1.make_move()
            player2_move = player2.make_move()

            outcome, turn_info = self.run_single_turn(player1_move,
                                                      player2_move,
                                                      player1,
                                                      player2)
            self.log_turn(turn_logwriter, turn_info)

        if outcome["draw"]:
            # It was a draw, decide randomly
            return int(random() < 0.5)

        return outcome["winner"]

    def run_single_turn(self, player1_move, player2_move, player1, player2):
        """
        Run the turn for these moves.

        Args:
            player1_move (tuple): Move chosen by player1.
            player2_move (tuple): Move chosen by player2.
            player1 (PokemonAgent): The object that is the first player.
            player2 (PokemonAgent): The object that is the second player.

        Returns:
            Information about the turn, as well as a dictionary with informaton on whether
                or not the game has ended.

        """
        turn_info = self.calculate_turn(player1_move, player2_move)

        # Go from player1/2 to the players' IDs
        player_id_dict = {
            "player1": player1.id,
            "player2": player2.id,
            None: None
        }
        for info in turn_info:
            if "player" in info:
                info["player"] = player_id_dict[info.get("player")]
            elif "attacker" in info:
                info["attacker"] = player_id_dict[info.get("attacker")]
                info["defender"] = player_id_dict[info.get("defender")]

        apply_status_damage(self.game_state["player1"]["active"])
        apply_status_damage(self.game_state["player2"]["active"])

        player1.new_info(turn_info)
        player2.new_info(turn_info)

        # Figure out who faints at the end of this turn.
        if self.game_state["player1"]["active"].current_hp <= 0:
            self.game_state["player1"]["active"] = None
        if self.game_state["player2"]["active"].current_hp <= 0:
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

        Args:
            move1 (tuple): Player 1's move. Tuple of size 2. First
                value is the type of move (either SWITCH or ATTACK),
                followed by the index of the attack or pokemon to be
                switched to.
            move2 (tuple): Player 2's move. See move1.

        Returns:
            List of the events that happened that turn.

        """
        p1_switch = move1[0] == "SWITCH"
        p2_switch = move2[0] == "SWITCH"

        turn_info = []

        if not p1_switch and not p2_switch:
            turn_info = self.turn_both_attack(move1, move2)
        elif p1_switch:
            turn_info.extend(self.switch_pokemon("player1", move1[1]))
            attack = self.game_state["player2"]["active"].moves[move2[1]]
            result = self.attack("player2", attack)
            if result is not None:
                turn_info.extend(result)
        elif p2_switch:
            turn_info.extend(self.switch_pokemon("player2", move2[1]))
            attack = self.game_state["player1"]["active"].moves[move1[1]]
            result = self.attack("player1", attack)
            if result is not None:
                turn_info.extend(result)
        else:
            turn_info.extend(self.switch_pokemon("player1", move1[1]))
            turn_info.extend(self.switch_pokemon("player2", move2[1]))

        return turn_info

    def switch_pokemon(self, player, position):
        """
        Switch a player's pokemon out.

        Args:
            player (str):  The player ("player1" or "player2") who is
                doing the switching.
            position (int): The position in the team that this player is
                switching out to.

        Returns:
            The information about the switch that was just performed.

        """
        # Reset boosts and volatile status
        self.game_state[player]["active"].boosts = default_boosts()
        self.game_state[player]["active"].volatile_status = {}

        # If toxic-ed, reset the turn counter
        if self.game_state[player]["active"].status == TOX_STATUS:
            self.game_state[player]["active"].status_turns = 0

        # Switch
        cur_active = self.game_state[player]["active"]
        self.game_state[player]["team"].append(cur_active)
        new_active = self.game_state[player]["team"].pop(position)
        self.game_state[player]["active"] = new_active

        # New Data
        results = {}
        results["type"] = "SWITCH"
        results["player"] = player
        results["old_active"] = cur_active.name
        results["new_active"] = new_active.name
        return [results]

    def attack(self, attacker, move):
        """
        Attack opposing pokemon with the move.

        Args:
            attacker (str): The player ("player1" or "player2")
                who is attacking.
            move (dict): The data for the move that is being done.

        Returns:
            List of the information on the attack that was just done.

        """
        # pylint: disable=R0912
        # Disable too many branches
        # I don't think there's a better way to do this

        # pylint: disable=R0914
        # Disable too many variables
        # Bite me I need these variables until I split this out

        # pylint: disable=R0915
        # Disable too many statements
        # Right now I don't have everything implemented, so I'll
        # wait until then to fully break this out.

        if attacker == "player1":
            defender = "player2"
        else:
            defender = "player1"

        atk_poke = self.game_state[attacker]["active"]
        def_poke = self.game_state[defender]["active"]

        # Check for paralysis
        if atk_poke.status == PAR_STATUS and random() < 0.25:
            return None
        # Check for freeze
        if atk_poke.status == FRZ_STATUS:
            # Check for player thaw
            if random() < 0.2 or move["type"] == "fire" or move["id"] == "scald":
                atk_poke.status = None
            else:
                return None
        # Check for sleep
        if atk_poke.status == SLP_STATUS:
            # Check for player wake up
            if random() < 1.0/3 or atk_poke.status_counter == 3:
                atk_poke.status = None
                atk_poke.status_counter = 0
            # Increment sleep counter
            else:
                atk_poke.status_counter += 1
                return None

        # Check if the move even hit...
        damage = 0
        critical_hit = False
        move_hits = move.check_hit()
        if move_hits:
            # Do Damage
            damage, critical_hit = move.calculate_damage(atk_poke, def_poke)
            def_poke.current_hp -= damage

            # Thaw opponent if applicable
            if def_poke.status == FRZ_STATUS and (move["type"] == "fire" or move["id"] == "scald"):
                def_poke.status = None

            # Healing
            if "heal" in move["flags"]:
                if "heal" in move and move["heal"]:
                    heal_factor = move["heal"][0]/move["heal"][1]
                else:
                    heal_factor = 0.5
                heal_amount = floor(heal_factor*atk_poke.max_hp)
                # No overheal
                atk_poke.current_hp = min(atk_poke.max_hp, atk_poke.current_hp + heal_amount)

            move.apply_boosts(atk_poke, def_poke)
            move.apply_volatile_status(atk_poke, def_poke)
            move.apply_secondary_effect(atk_poke, def_poke)

        # Increment VolatileStatus counter for attack Pokemon
        for vol_status in atk_poke.volatile_status:
            if vol_status == "lockedmove":
                atk_poke.volatile_status[vol_status]["counter"] += 1
            elif vol_status != "substitute":
                atk_poke.volatile_status[vol_status] += 1

        results = {}
        results["type"] = "ATTACK"
        results["move"] = move
        results["critical_hit"] = critical_hit
        results["damage"] = damage
        results["pct_damage"] = 100*damage/def_poke.max_hp
        results["attacker"] = attacker
        results["defender"] = defender
        results["atk_poke"] = atk_poke.name
        results["def_poke"] = def_poke.name
        results["move_hits"] = move_hits
        return [results]

    def turn_both_attack(self, move1, move2):
        """
        Run a turn where both players attack.

        Args:
            move1 (dict): Player 1's attack.
            move2 (dict): Player 2's attack.

        Returns:
            List of the events that happened that turn.

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
        if new_data is not None:
            results.extend(new_data)
        if self.game_state[slower_player]["active"].current_hp > 0:
            new_data = self.attack(slower_player, move_dict[slower_player])
            if new_data is not None:
                results.extend(new_data)

        return results

    def win_condition_met(self):
        """
        Determine whether or not condition for victory is met.

        Either all of one player's pokemon have fainted (in which
        case it is a victory), or maximum number of turns allowed
        have passed.

        Returns:
            Dict with information whether or not the game is over, and
                (if applicable) who won the game.

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

        Args:
            player_id (str): The player whose data needs to be anonymized.
                Either "player1" or "player2".

        Returns:
            The anonymized game state for that player.

        """
        data = deepcopy(self.game_state[player_id])
        return anonymize_gamestate_helper(data)

    def turn_order(self, p1_move, p2_move):
        """
        Calculate turn order for when players move.

        Args:
            p1_move (dict): Player 1's move for this turn.
            p2_move (dict): Player 2's move for this turn.

        Returns:
            Tuple of 'player1', 'player2' in the order their moves
                will be made.

        """
        if p1_move["priority"] != p2_move["priority"]:
            if p1_move["priority"] > p2_move["priority"]:
                faster_player = "player1"
                slower_player = "player2"
            else:
                faster_player = "player2"
                slower_player = "player1"
        else:
            p1_speed = self.game_state["player1"]["active"].effective_stat("spe")
            p2_speed = self.game_state["player2"]["active"].effective_stat("spe")

            if p1_speed == p2_speed:
                # Speed tie, coin flip
                if random() > 0.5:
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
        """
        Update the player's gamestates to reflect the engine's gamestate.

        Args:
            player1 (PokemonAgent): The object that is the first player.
            player2 (PokemonAgent): The object that is the second player.

        """
        player1.update_gamestate(
            self.game_state["player1"], self.anonymize_gamestate("player2"))
        player2.update_gamestate(
            self.game_state["player2"], self.anonymize_gamestate("player1"))

    def log_turn(self, turn_logwriter, turn_info):
        """
        Log the information from this turn.

        Args:
            turn_logwriter (LogWriter): The LogWriter responsible for logging this
                battle's information.
            turn_info (list): The events that happened this turn.

        """
        if not self.log_turn_flag:
            return

        for turn in turn_info:
            if turn["type"] == "SWITCH":
                continue

            new_line = {}
            new_line["turn_num"] = self.game_state["num_turns"]
            new_line["player_id"] = turn["attacker"]
            new_line["active"] = turn["atk_poke"]
            new_line["target"] = turn["def_poke"]
            new_line["move"] = turn["move"]["id"]
            new_line["damage"] = turn["damage"]
            turn_logwriter.write_line(new_line)


def apply_status_damage(pokemon):
    """
    Apply damage for status conditions when appropriate.

    Args:
        pokemon (Pokemon): The pokemon that this damage is calculated for.

    """
    if pokemon.status is None:
        return

    dmg_pct = calculate_status_damage(pokemon)
    if pokemon.status == TOX_STATUS:
        # Increment toxic counter
        pokemon.status_turns += 1

    pokemon.current_hp -= floor(pokemon.max_hp*dmg_pct)


def anonymize_gamestate_helper(data):
    """
    Anonymize some gamestate data.

    Raw HP should be converted to percents. EV/Nature info is hidden,
    otherwise all info is preserved.

    Args:
        data (dict): The player's game state to be anonymized.

    Returns:
        Anonimyzed representation of the game state.

    """
    anon_data = {}

    anon_data["team"] = []
    for pokemon in data["team"]:
        pct_hp = pokemon.current_hp/pokemon.max_hp
        name = pokemon.name
        status = pokemon.status
        anon_data["team"].append({
            "name": name,
            "pct_hp": pct_hp,
            "status": status,
            "dex_num": pokemon.dex_num,
            "status_turns": pokemon.status_turns
        })

    if data["active"] is not None:
        anon_data["active"] = {
            "name": data["active"].name,
            "pct_hp": data["active"].current_hp/data["active"].max_hp,
            "boosts": data["active"].boosts,
            "status": data["active"].status,
            "dex_num": data["active"].dex_num,
            "status_turns": data["active"].status_turns
        }
    else:
        anon_data["active"] = None

    return anon_data


def init_player_logwriter(player1, player2):
    """
    Initialize the log writer to write the turns of this game.

    Args:
        player1 (PokemonAgent): The object that is Player 1.
        player2 (PokemonAgent): The object that is Player 2.

    Returns:
        The log writer for a battle between player1 and player2.

    """
    header = ["turn_num", "player_id", "active", "target", "move", "damage"]
    turn_logwriter = LogWriter(header, prefix="PKMNGame_{}_{}_{}".format(
        player1.type,
        player2.type,
        uuid4()))

    return turn_logwriter
