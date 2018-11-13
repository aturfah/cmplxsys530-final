"""Pokemon agent who's moves are determined by maximizing personal gain."""

import operator
from copy import deepcopy

from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_pokemon_agent import calc_opp_position_helper, calc_position_helper
from config import USAGE_STATS, POKEMON_DATA, MOVE_DATA
from config import (PAR_STATUS)
from pokemon_helpers.calculate import calc_boost_factor
from pokemon_helpers.calculate import calculate_status_damage


class BasicPlanningPokemonAgent(PokemonAgent):
    """
    Class for PokemonAgent who calculates the next move by maximizing some function.

    This agent will maximize the game_position given the opponent's moves are all
    equally likely.

    Attributes:
        tier (str): Tier to look at usage stats for.

    """

    def __init__(self, tier, **kwargs):
        """Initialize a player with a specific tier."""
        team = kwargs["team"]
        super().__init__(team)
        self.tier = tier

    def make_move(self):
        """
        Choose the move to make.

        Returns:
            Tuple of move type (SWITCH or ATTACK) and position.

        """
        player_opts, opp_opts = self.generate_possibilities()
        move_choice = self.optimal_move(player_opts, opp_opts)
        return move_choice

    def generate_possibilities(self):
        """
        Generate a two lists of possible player and opponent moves.

        Returns:
            Lists of possible player and opponent moves, given the gamestate.

        """
        player_opts = []
        opp_opts = []

        # My possible attacks
        posn = 0
        for _ in self.game_state.gamestate["active"].moves:
            player_opts.append(("ATTACK", posn))
            posn += 1

        # My possible switches
        posn = 0
        for _ in self.game_state.gamestate["team"]:
            player_opts.append(("SWITCH", posn))
            posn += 1

        # Opponent's possible attacks
        posn = 0
        opp_active_poke = self.game_state.opp_gamestate["data"]["active"]["name"]
        opp_moves = []
        if opp_active_poke in self.game_state.opp_gamestate["moves"]:
            for move in self.game_state.opp_gamestate["moves"][opp_active_poke]:
                opp_moves.append(move["id"])

        if len(opp_moves) < 4:
            # Infer remaining moves from tier's data
            common_moves = USAGE_STATS[self.tier][opp_active_poke]["Moves"]
            common_moves = sorted(common_moves.items(),
                                  key=operator.itemgetter(1), reverse=True)
            common_moves = [move[0] for move in common_moves if move[0] != ""]
            for move in common_moves:
                if move not in opp_moves:
                    opp_moves.append(move)
                if len(opp_moves) == 4:
                    break

        for move in opp_moves:
            opp_opts.append(("ATTACK", move))

        # Opponent's possible switches
        posn = 0
        for _ in self.game_state.opp_gamestate["data"]["team"]:
            opp_opts.append(("SWITCH", posn))
            posn += 1

        return player_opts, opp_opts

    def optimal_move(self, player_opts, opp_opts):
        """
        Choose the optimal move given the options availible.

        Args:
            player_opts (list): List of the player's moves for this turn.
            opp_opts (list): List of the opponent's moves for this turn.

        Returns:
            Player move that optimizes the battle_position function for this agent.

        """
        optimal_opt = None
        maximal_position = -1
        for p_opt in player_opts:
            total_position = 0
            # Calculate outcomes based on possible misses
            player_outcomes, player_weights = self.calc_move_outcomes(p_opt, True)

            # Calculate average position given opponent's possible moves
            for o_opt in opp_opts:
                # Calculate outcomes based on possible misses
                opp_outcomes, opp_weights = self.calc_move_outcomes(o_opt, False)

                for p_ind, p_outc in enumerate(player_outcomes):
                    for o_ind, o_outc in enumerate(opp_outcomes):
                        my_gs = deepcopy(self.game_state.gamestate)
                        opp_gs = deepcopy(self.game_state.opp_gamestate)

                        my_gs, opp_gs = self.apply_moves()

                        # Weighted update of the position
                        total_position += self.position_func(my_gs=my_gs,
                                                             opp_gs=opp_gs,
                                                             player_weight=player_weights[p_ind],
                                                             opp_weight=opp_weights[o_ind])

            # Calculate expected position for this move
            avg_position = total_position / len(opp_opts)
            if avg_position > maximal_position:
                optimal_opt = p_opt
                maximal_position = avg_position

        return optimal_opt

    def attacking_dmg_range(self, my_gs, opp_gs, p_opt):
        """
        Calculate the (weighted) damage range for an attack.

        Args:
            my_gs (dict): This player's game state as a dictionary.
            opp_gs (dict): The opponent's game state as a dictionary.
            p_opt (tuple): The player's choice for this turn.

        Returns:
            Expected damage range for an attack.
                Damage is calculated with each possible investment as equally likely.

        """
        p_poke = my_gs["active"]
        p_move = p_poke.moves[p_opt[1]]
        o_poke_name = opp_gs["data"]["active"]["name"]
        o_poke = POKEMON_DATA[o_poke_name]
        params = self.game_state.opp_gamestate["investment"][o_poke_name]

        # We do not handle status moves at this point in time.
        if p_move["category"] == "Status":
            return [0, 0]

        # Get sum of damage ranges
        dmg_range = None
        param_combs = atk_param_combinations(p_poke, params, p_move)
        for param_comb in param_combs:
            dmg_val = self.dmg_stat_calc.calculate_range(p_move, p_poke, o_poke, param_comb)
            if not dmg_range:
                dmg_range = [0, 0]

            dmg_range[0] += dmg_val[0]
            dmg_range[1] += dmg_val[1]

        # Each combination is weighted equally
        dmg_range[0] = dmg_range[0] / len(param_combs)
        dmg_range[1] = dmg_range[1] / len(param_combs)

        return dmg_range

    def defending_dmg_range(self, my_gs, opp_gs, o_opt):
        """
        Calculate the (weighted) damage range when attacked.

        Args:
            my_gs (dict): This player's (potential) game state.
            opp_gs (dict): The opponent's game state as a dictionary.
            o_opt (tuple): The opponent's choice for this turn.

        Returns:
            Expected damage range for an opponent's attack.
                Damage is calculated with each possible investment as equally likely.

        """
        p_poke = my_gs["active"]
        o_move = MOVE_DATA[o_opt[1]]
        o_poke_name = opp_gs["data"]["active"]["name"]
        o_poke = POKEMON_DATA[o_poke_name]
        o_poke["status"] = opp_gs["data"]["active"]["status"]
        params = self.game_state.opp_gamestate["investment"][o_poke_name]

        # We do not handle status moves at this point in time.
        if o_move["category"] == "Status":
            return [0, 0]

        dmg_range = None
        param_combs = def_param_combinations(p_poke, params, o_move)
        for param_comb in param_combs:
            dmg_val = self.dmg_stat_calc.calculate_range(o_move, o_poke, p_poke, param_comb)
            if not dmg_range:
                dmg_range = [0, 0]

            dmg_range[0] += dmg_val[0]
            dmg_range[1] += dmg_val[1]

        # Each combination is weighted equally
        dmg_range[0] = dmg_range[0] / len(param_combs)
        dmg_range[1] = dmg_range[1] / len(param_combs)

        return dmg_range

    def update_opp_gs_atk(self, my_gs, opp_gs, p_opt):
        """
        Update opponent gamestate when we're attacking.

        Args:
            my_gs (dict): This player's game state as a dictionary.
            opp_gs (dict): The opponent's game state as a dictionary.
            p_opt (tuple): The player's choice for this turn.

        Returns:
            Updated opponent's game state for the attack.

        """
        dmg_range = self.attacking_dmg_range(my_gs, opp_gs, p_opt)

        # Average damage as decimal
        opp_gs["data"]["active"]["pct_hp"] -= (dmg_range[0] + dmg_range[1]) / 200

        # Control for being less than zero
        if opp_gs["data"]["active"]["pct_hp"] < 0:
            opp_gs["data"]["active"]["pct_hp"] = 0
        return opp_gs

    def update_my_gs_def(self, my_gs, opp_gs, o_opt):
        """
        Update my_gs variable when on defense.

        Args:
            my_gs (dict): This player's game state as a dictionary.
            opp_gs (dict): The opponent's game state as a dictionary.
            o_opt (tuple): The opponent's choice for this turn.

        Returns:
            Updated player gamestate given the opponent's attack.

        """
        dmg_range = self.defending_dmg_range(my_gs, opp_gs, o_opt)

        # Average damage as portion of total HP
        my_gs["active"].current_hp -= my_gs["active"].max_hp * \
            (dmg_range[0] + dmg_range[1]) / 200

        # Control for being less than zero
        if my_gs["active"].current_hp < 0:
            my_gs["active"].current_hp = 0

        return my_gs

    def determine_faster(self, my_gs, opp_gs, p_opt, o_opt):
        """
        Determine whether this player is faster.

        Args:
            my_gs (dict): This player's game state as a dictionary.
            opp_gs (dict): The opponent's game state as a dictionary.
            p_opt (tuple): The player's choice for this turn.
            o_opt (tuple): The opponent's choice for this turn.

        Returns:
            Boolean whether or not this player is faster than the opponent.

        """
        p_poke = my_gs["active"]
        o_poke_name = opp_gs["data"]["active"]["name"]

        p_move = p_poke.moves[p_opt[1]]
        o_move = MOVE_DATA[o_opt[1]]

        # Same priority is decided by speed
        if p_move["priority"] == o_move["priority"]:
            speed_pairs = self.game_state.opp_gamestate["investment"][o_poke_name]["spe"]
            min_opp_spe, max_opp_spe = speed_pairs

            # Factor in status
            opp_modifier = 1
            if opp_gs["data"]["active"]["status"] == PAR_STATUS:
                opp_modifier = opp_modifier * 0.5

            # Factor in Boosts
            opp_modifier = opp_modifier * calc_boost_factor(opp_gs["data"]["active"], "spe")

            # Assume that any speed is possible, which isn't exactly correct
            return p_poke.effective_stat("spe") > opp_modifier * (min_opp_spe + max_opp_spe) / 2

        # Moves of different priority will always go in priority order
        return p_move["priority"] > o_move["priority"]

    def calc_move_outcomes(self, move_opt, player_flag=True):
        """
        For a move, generate possible outcomes.

        Considers Hit/Miss.

        Args:
            player_flag (bool): Whether to use player or opponent's gamestate.

        Returns:
            List of possible outcomes and their weights.

        """
        possible_outcomes = [move_opt + (True, )]
        outcome_weights = [1]
        if move_opt[0] == "ATTACK":
            if player_flag:
                chosen_move = self.game_state.gamestate["active"].moves[move_opt[1]]
            else:
                chosen_move = MOVE_DATA[move_opt[1]]

            acc = chosen_move["accuracy"]
            if not isinstance(acc, bool) and acc < 100:
                outcome_weights = [(1.0 * val)/100 for val in [acc, 100 - acc]]
                possible_outcomes = [move_opt + (val == acc, ) for val in [acc, 100 - acc]]

        return possible_outcomes, outcome_weights

    def position_func(self, *args, **kwargs):
        """
        Determine battle position for game state, given the probabilities.

        Args:
            my_gs (dict):
            opp_gs (dict):
            player_weight (float):
            opp_weight (float):

        Returns:
            Factor for this outcome's weight in the move choice.

        """
        # pylint: disable=R0201
        # This needs to be over-ridden by child class
        if args:
            raise RuntimeWarning("Args is ignored.")

        my_posn = calc_position_helper(kwargs["my_gs"]) + 0.01
        opp_posn = calc_opp_position_helper(kwargs["opp_gs"]) + 0.01

        return (my_posn / opp_posn) * (kwargs["player_weight"] * kwargs["opp_weight"])

    def handle_logic_both_attacking(self, my_gs, opp_gs, p_opt, o_opt, p_outc, o_outc):
        """Placeholder Docstring."""
        # Figure out who is faster
        if self.determine_faster(my_gs, opp_gs, p_opt, o_opt):
            # We attack first, then opponent attacks
            if p_outc[2]:
                # Check if we miss
                opp_gs = self.update_opp_gs_atk(my_gs, opp_gs, p_opt)

            if opp_gs["data"]["active"]["pct_hp"] > 0 and o_outc[2]:
                # Check that opponent is still alive and doesn't miss
                my_gs = self.update_my_gs_def(my_gs, opp_gs, o_opt)
        else:
            # Opponent attacks first, then us
            if o_outc[2]:
                # Check if opponent misses
                my_gs = self.update_my_gs_def(my_gs, opp_gs, o_opt)

            if my_gs["active"].current_hp > 0 and p_outc[2]:
                # Check that we are still alive and don't miss
                opp_gs = self.update_opp_gs_atk(my_gs, opp_gs, p_opt)

        return my_gs, opp_gs

    def apply_moves(self, my_gs, opp_gs, p_opt, o_opt, p_outc, o_outc):
        """Placeholder Docstring."""
        # Player Switches
        if p_opt[0] == "SWITCH":
            my_gs = update_gs_switch(my_gs, p_opt)

        # Opponent Switches
        if o_opt[0] == "SWITCH":
            opp_gs = update_gs_switch(opp_gs, o_opt, False)

        # Attacking
        if p_opt[0] == "ATTACK" and o_opt[0] == "ATTACK":
            my_gs, opp_gs = self.handle_logic_both_attacking(my_gs, opp_gs,
                                                             p_opt, o_opt,
                                                             p_outc, o_outc)

        elif p_opt[0] == "ATTACK" and p_outc[2]:
            # Only we attack, and we don't miss
            opp_gs = self.update_opp_gs_atk(my_gs, opp_gs, p_opt)

        elif o_opt[0] == "ATTACK" and o_outc[2]:
            # Only opponent attacks, and doesn't miss
            my_gs = self.update_my_gs_def(my_gs, opp_gs, o_opt)

        # Apply status damage
        my_gs["active"].current_hp -= my_gs["active"].current_hp * \
            calculate_status_damage(my_gs["active"])
        opp_gs["data"]["active"]["pct_hp"] -= \
            calculate_status_damage(opp_gs["data"]["active"])

        # Control for damage falling below zero
        my_gs["active"].current_hp = max(my_gs["active"].current_hp, 0)
        opp_gs["data"]["active"]["pct_hp"] = max(opp_gs["data"]["active"]["pct_hp"], 0.0)

        return my_gs, opp_gs

def atk_param_combinations(active_poke, opp_params, move):
    """
    Calculate possible parameter combinations for when we're attacking.

    Args:
        active_poke (Pokemon): This player's active (attacking) Pokemon.
        opp_params (dict): The opponent's investment inference.
        move (dict): The move that is being attacked with.

    Returns:
        List of possible investment combinations when attacking.

    """
    results = []

    # Figure out which stat we should use
    stat = "atk"
    opp_stat = "def"
    if move["category"] == "Special":
        stat = "spa"
        opp_stat = "spd"

    result_dict = {}
    result_dict["atk"] = {}

    # Set the values for the player's pokemon investment
    if stat in active_poke.evs and active_poke.evs[stat] > 128:
        result_dict["atk"]["max_evs"] = True
    if active_poke.increase_stat == stat:
        result_dict["atk"]["positive_nature"] = True

    # Set the values for the opponent's investment
    for hp_params in opp_params["hp"]:
        for def_params in opp_params[opp_stat]:
            temp_results = deepcopy(result_dict)
            temp_results["hp"] = hp_params
            temp_results["def"] = def_params
            results.append(temp_results)

    return results


def def_param_combinations(active_poke, opp_params, move):
    """
    Parameter combinations for when we're on the defensive.

    Args:
        active_poke (Pokemon): This player's active (attacking) Pokemon.
        opp_params (dict): The opponent's investment inference.
        move (dict): The move that is being attacked with.

    Returns:
        List of possible investment combinations when on the defensive.

    """
    results = []

    # Figure out which stat we should use
    stat = "def"
    opp_stat = "atk"
    if move["category"] == "Special":
        stat = "spd"
        opp_stat = "spa"

    result_dict = {}
    result_dict["def"] = {}
    result_dict["hp"] = {}

    # Information for Defense Stat
    if stat in active_poke.evs and active_poke.evs[stat] > 128:
        result_dict["def"]["max_evs"] = True
    if active_poke.increase_stat == stat:
        result_dict["def"]["positive_nature"] = True

    # Information for HP Stat
    if "hp" in active_poke.evs and active_poke.evs["hp"] > 128:
        result_dict["hp"]["max_evs"] = True

    for atk_params in opp_params[opp_stat]:
        temp_results = deepcopy(result_dict)
        temp_results["atk"] = atk_params
        results.append(temp_results)

    return results


def update_gs_switch(gamestate, opt, my_gs=True):
    """
    Update the gamestate on switch.

    Args:
        gamestate (dict): The gamestate to be updated
        opt (tuple): The move that was made by the player
        my_gs (bool): Flag whether or not this is the player's gamestate to be updated.
    """
    if my_gs:
        temp = gamestate["active"]
        gamestate["active"] = gamestate["team"][opt[1]]
        gamestate["team"].pop(opt[1])
        gamestate["team"].append(temp)
    else:
        temp = gamestate["data"]["active"]
        gamestate["data"]["active"] = gamestate["data"]["team"][opt[1]]
        gamestate["data"]["team"].pop(opt[1])
        gamestate["data"]["team"].append(temp)

    return gamestate
