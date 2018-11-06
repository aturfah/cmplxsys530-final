"""Class defining an Engine's Game State."""

from config import POKEMON_DATA

from pokemon_helpers.pokemon import Pokemon
from pokemon_helpers.calculate import calculate_spe_range
from pokemon_helpers.calculate import generate_all_ev_combinations
from pokemon_helpers.damage_stats import DamageStatCalc


class PokemonPlayerGameState:
    """Representation of a player's internal game state."""

    def __init__(self):
        """Initialize this player's internal game state."""
        self.test_attr = {}
        self.gamestate = {}
        self.opp_gamestate = {}
        self.opp_gamestate["data"] = {}
        self.opp_gamestate["moves"] = {}
        self.opp_gamestate["investment"] = {}
        self.dmg_stat_calc = DamageStatCalc()

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.gamestate = {}
        self.opp_gamestate = {}
        self.opp_gamestate["data"] = {}
        self.opp_gamestate["moves"] = {}
        self.opp_gamestate["investment"] = {}

    def init_opp_gamestate(self, opp_team, opp_active):
        """
        Initialize the investment data for the opponent's team.

        Args:
            opp_team (list): List with the opponent's Pokemon.
            opp_active (Pokemon): Opponent's active Pokemon.

        """
        possible_combs = generate_all_ev_combinations()
        self.opp_gamestate["investment"][opp_active["name"]] = {}
        self.opp_gamestate["investment"][opp_active["name"]]["hp"] = possible_combs["hp"]
        self.opp_gamestate["investment"][opp_active["name"]]["atk"] = possible_combs["atk"]
        self.opp_gamestate["investment"][opp_active["name"]]["def"] = possible_combs["def"]
        self.opp_gamestate["investment"][opp_active["name"]]["spa"] = possible_combs["spa"]
        self.opp_gamestate["investment"][opp_active["name"]]["spd"] = possible_combs["spd"]
        self.opp_gamestate["investment"][opp_active["name"]]["spe"] = \
            calculate_spe_range(opp_active["name"])

        for opp_poke in opp_team:
            self.opp_gamestate["investment"][opp_poke["name"]] = {}
            self.opp_gamestate["investment"][opp_poke["name"]]["hp"] = possible_combs["hp"]
            self.opp_gamestate["investment"][opp_poke["name"]]["atk"] = possible_combs["atk"]
            self.opp_gamestate["investment"][opp_poke["name"]]["def"] = possible_combs["def"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spa"] = possible_combs["spa"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spd"] = possible_combs["spd"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spe"] = \
                calculate_spe_range(opp_poke["name"])

    def update_gamestate(self, my_gamestate, opp_gamestate):
        """
        Update internal gamestate for self.

        Args:
            my_gamestate (dict): PokemonEngine representation of player's position.
                Should have "active" and "team" keys.
            opp_gamestate (dict): PokemonEngine representation of opponent's position.
                Only % HP should be viewable, and has "active" and "team" keys.

        """
        self.gamestate = my_gamestate
        self.opp_gamestate["data"] = opp_gamestate

    def new_info(self, raw_turn_info, my_id):
        """
        Get new info for opponent's game_state.

        Assumes Species Clause is in effect.

        Args:
            turn_info (list): What happened on that turn, who took what damage.
            my_id (str): Name corresponding to the "attacker" or "defender"
                values of this dict. To know which values the method
                should be looking at in turn_info.
        """
        turn_info = [turn for turn in raw_turn_info if turn["type"] == "ATTACK"]

        for info in turn_info:
            if "critical_hit" in info and info["critical_hit"]:
                # Modify damage for critical hits
                info["damage"] = info["damage"]*2/3
                info["pct_damage"] = info["pct_damage"]*2/3

            if info["attacker"] == my_id:
                # We attacked, infer data about defending pokemon
                if info.get("move_hits", True):
                    results, combinations = self.results_attacking(info)
                    self.update_atk_inference(info, results, combinations)
            else:
                # Just got attacked, infer data about attacking pokemon
                if info.get("move_hits", True):
                    results, combinations = self.results_defending(info)
                    self.update_def_inference(info, results, combinations)

                # We're the defender, just learned about a move
                opp_name = self.opp_gamestate["data"]["active"]["name"]

                if opp_name not in self.opp_gamestate["moves"]:
                    self.opp_gamestate["moves"][opp_name] = []
                if info["move"] not in self.opp_gamestate["moves"][opp_name]:
                    self.opp_gamestate["moves"][opp_name].append(info["move"])

        if len(turn_info) == 2 and not contains_switch(turn_info):
            self.update_speed_inference(turn_info, my_id)

    def update_speed_inference(self, turn_info, my_id):
        """
        Infer speed information from the turn info.

        Args:
            turn_info (dict): Information on a single event of that turn.
            my_id (str): Name corresponding to the "attacker" or "defender"
                values of this dict.

        """
        # Moves are different priority, no inference can be made
        if turn_info[0]["move"]["priority"] != turn_info[1]["move"]["priority"]:
            return

        # We're outsped; ie: we're slower
        opp_poke = turn_info[0]["atk_poke"]
        outspeed = False
        if turn_info[0]["attacker"] == my_id:
            # We outspeed; ie: we're faster
            opp_poke = turn_info[0]["def_poke"]
            outspeed = True

        if opp_poke not in self.opp_gamestate["investment"]:
            self.opp_gamestate["investment"][opp_poke] = {}
        if "spe" not in self.opp_gamestate["investment"][opp_poke]:
            # Slowest possible opponent's pokemon
            min_speed = Pokemon(name=opp_poke, moves=["tackle"], nature="brave").speed
            # Fastest possible opponent's pokemon
            max_speed = Pokemon(name=opp_poke,
                                moves=["tackle"],
                                evs={"spe": 252},
                                nature="jolly").speed
            self.opp_gamestate["investment"][opp_poke]["spe"] = [min_speed, max_speed]

        if outspeed:
            if self.opp_gamestate["investment"][opp_poke]["spe"][1] > \
                    self.gamestate["active"].speed:
                # Update maximum speed to our speed if necessary
                self.opp_gamestate["investment"][opp_poke]["spe"][1] = \
                    self.gamestate["active"].speed
        else:
            if self.opp_gamestate["investment"][opp_poke]["spe"][0] < \
                    self.gamestate["active"].speed:
                # Update minimum speed to our speed, if necessary
                self.opp_gamestate["investment"][opp_poke]["spe"][0] = \
                    self.gamestate["active"].speed

    def results_attacking(self, turn_info):
        """
        Generate possible results for when we are attacking.

        Args:
            turn_info (dict): Information on a single event of that turn.

        Returns:
            Two lists contianing T/F values of opponent's defense investment.

        """
        move = turn_info["move"]
        my_poke = POKEMON_DATA[turn_info["def_poke"]]
        opp_poke = POKEMON_DATA[turn_info["atk_poke"]]

        params = {}
        params["atk"] = {}
        if self.gamestate["active"].evs.get("atk", 0) > 124:
            params["atk"]["max_evs"] = True
        if self.gamestate["active"].increase_stat == "attack":
            params["atk"]["positive_nature"] = True

        params["def"] = {}
        params["hp"] = {}

        combinations = []
        combinations.append((False, False, False))
        combinations.append((False, False, True))
        combinations.append((True, False, False))
        combinations.append((True, False, True))
        combinations.append((False, True, False))
        combinations.append((False, True, True))
        combinations.append((True, True, False))
        combinations.append((True, True, True))
        num_combinations = len(combinations)

        results = []
        for comb_ind in range(num_combinations):
            comb = combinations[comb_ind]
            params["def"]["max_evs"] = comb[0]
            params["def"]["positive_nature"] = comb[1]
            params["hp"]["max_evs"] = comb[2]

            results.append(self.dmg_stat_calc.calculate_range(move, opp_poke, my_poke, params))

        return results, combinations

    def results_defending(self, turn_info):
        """
        Generate possible results for when we are defending.

        Args:
            turn_info (dict): Information on a single event of that turn.

        Returns:
            Two lists contianing T/F values of opponent's defense investment.

        """
        move = turn_info["move"]
        my_poke = POKEMON_DATA[turn_info["def_poke"]]
        opp_poke = POKEMON_DATA[turn_info["atk_poke"]]

        params = {}
        params["atk"] = {}

        params["def"] = {}
        if self.gamestate["active"].evs.get("def", 0) > 124:
            params["def"]["max_evs"] = True
        if self.gamestate["active"].increase_stat == "defense":
            params["def"]["positive_nature"] = True

        params["hp"] = {}
        if self.gamestate["active"].evs.get("hp", 0) > 124:
            params["hp"]["max_evs"] = True

        combinations = []
        combinations.append((False, False))
        combinations.append((True, False))
        combinations.append((False, True))
        combinations.append((True, True))

        results = []
        for comb_ind in range(4):
            comb = combinations[comb_ind]
            params["atk"]["max_evs"] = comb[0]
            params["atk"]["positive_nature"] = comb[1]

            results.append(self.dmg_stat_calc.calculate_range(
                move, opp_poke, my_poke, params))

        return results, combinations

    def valid_results_atk(self, poke_name, stat, dmg_pct, results, combinations):
        """
        Decide which of potential the potential results are valid given damage dealt.

        Args:
            poke_name (str): Name of the pokemon in question.
            stat (str): Name of the statistic that this move's damage is
                calculated from, defense or special defense.
            dmg_pct (float): How much % damage was done this turn.
            results (list): Possible defense investment combinations.
            combinations (list): T/F values corresponding to the defense investment combinations.

        Returns:
            Subset of the results that are possible given the damage dealt.

        """
        valid_results = []
        num_results = len(results)

        # Initialize the data for this pokemon if not already there
        if poke_name not in self.opp_gamestate["investment"]:
            self.opp_gamestate["investment"][poke_name] = {}

        if stat not in self.opp_gamestate["investment"][poke_name]:
            self.opp_gamestate["investment"][poke_name][stat] = []
            self.opp_gamestate["investment"][poke_name]["hp"] = []

        for result_ind in range(num_results):
            result = results[result_ind]
            if result[0] <= dmg_pct <= result[1]:
                result_dict = {}
                result_dict[stat] = {}
                result_dict["hp"] = {}
                result_dict[stat]["max_evs"] = combinations[result_ind][0]
                result_dict[stat]["positive_nature"] = combinations[result_ind][1]
                result_dict["hp"]["max_evs"] = combinations[result_ind][2]
                valid_results.append(result_dict)

        return valid_results

    def valid_results_def(self, poke_name, stat, dmg_pct, results, combinations):
        """
        Decide which of potential the potential results are valid given damage dealt.

        Args:
            poke_name (str): Name of the pokemon in question.
            stat (str): Name of the statistic that this move's damage is
                calculated from, defense or special defense.
            dmg_pct (float): How much % damage was done this turn.
            results (list): Possible defense investment combinations.
            combinations (list): T/F values corresponding to the defense investment combinations.

        Returns:
            Subset of the results that are possible given the damage dealt.

        """
        valid_results = []
        num_results = len(results)

        if poke_name not in self.opp_gamestate["investment"]:
            self.opp_gamestate["investment"][poke_name] = {}

        if stat not in self.opp_gamestate["investment"][poke_name]:
            self.opp_gamestate["investment"][poke_name][stat] = []

        for result_ind in range(num_results):
            result = results[result_ind]
            if result[0] <= dmg_pct <= result[1]:
                result_dict = {}
                result_dict["max_evs"] = combinations[result_ind][0]
                result_dict["positive_nature"] = combinations[result_ind][1]
                valid_results.append(result_dict)

        return valid_results

    def update_atk_inference(self, turn_info, results, combinations):
        """
        Update the opponent's defense investment information.

        Args:
            turn_info (dict): Information on damage dealt this turn.
            results (list): Possible defense investment combinations.
            combinations (list): T/F values corresponding to the defense investment combinations.

        """
        move = turn_info["move"]
        dmg_pct = turn_info["pct_damage"]

        stat = "def"
        if move["category"] != "Physical":
            stat = "spd"
        poke_name = turn_info["def_poke"]
        valid_results = self.valid_results_atk(poke_name, stat, dmg_pct, results, combinations)

        if not self.opp_gamestate["investment"][poke_name][stat]:
            for res in valid_results:
                self.opp_gamestate["investment"][poke_name][stat].append(res[stat])
                self.opp_gamestate["investment"][poke_name]["hp"].append(res["hp"])
        else:
            def_results = [res[stat] for res in valid_results]
            hp_results = [res["hp"] for res in valid_results]

            self.opp_gamestate["investment"][poke_name][stat] = [
                result for result in def_results
                if result in self.opp_gamestate["investment"][poke_name][stat]
            ]

            self.opp_gamestate["investment"][poke_name]["hp"] = [
                result for result in hp_results
                if result in self.opp_gamestate["investment"][poke_name]["hp"]
            ]

            # Stop it from becoming empty
            if not self.opp_gamestate["investment"][poke_name][stat]:
                self.opp_gamestate["investment"][poke_name][stat] = \
                        generate_all_ev_combinations()[stat]
            if not self.opp_gamestate["investment"][poke_name]["hp"]:
                self.opp_gamestate["investment"][poke_name]["hp"] = \
                        generate_all_ev_combinations()["hp"]

    def update_def_inference(self, turn_info, results, combinations):
        """
        Update the opponent's attack investment information.

        Args:
            turn_info (dict): Information on damage dealt this turn.
            results (list): Possible defense investment combinations.
            combinations (list): T/F values corresponding to the defense investment combinations.

        """
        move = turn_info["move"]
        dmg_pct = turn_info["pct_damage"]

        stat = "atk"
        if move["category"] != "Physical":
            stat = "spa"
        poke_name = turn_info["atk_poke"]
        valid_results = self.valid_results_def(poke_name, stat, dmg_pct, results, combinations)

        if not self.opp_gamestate["investment"][poke_name][stat]:
            self.opp_gamestate["investment"][poke_name][stat] = valid_results
        else:
            self.opp_gamestate["investment"][poke_name][stat] = [
                result for result in valid_results
                if result in self.opp_gamestate["investment"][turn_info["atk_poke"]][stat]
            ]

        # Stop it from becoming empty
        if not self.opp_gamestate["investment"][poke_name][stat]:
            self.opp_gamestate["investment"][poke_name][stat] = \
                    generate_all_ev_combinations()[stat]

    def __getitem__(self, key):
        """
        Define [] lookup on this object.

        Args:
            key (str): Attribute of this object to get.

        Returns:
            Attribute of this object at the key.

        """
        return self.__getattribute__(key)

    def to_json(self):
        """Convert this instance to something the interface can use."""
        output = {}

        # Add the player's gamestate info
        output["player"] = {}
        output["player"]["active"] = self.gamestate["active"].to_json()
        output["player"]["team"] = [pkmn.to_json() for pkmn in self.gamestate["team"]]

        # Add opponent's info
        output["opponent"] = self.opp_gamestate

        return output


def contains_switch(turn_info):
    """
    Determine if switching info contains Switch information.

    Args:
        turn_info (list): List of event that happened that turn.

    Returns:
        Boolean whether or not a switch happened that turn.

    """
    for info in turn_info:
        if info["type"] == "SWITCH":
            return True

    return False
