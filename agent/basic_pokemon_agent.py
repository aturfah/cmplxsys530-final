"""Class for a pokemon player."""

from numpy.random import uniform
from agent.base_agent import BaseAgent
from pokemon_helpers.damage_stats import DamageStatCalc
from pokemon_helpers.pokemon import Pokemon

from config import POKEMON_DATA


class PokemonAgent(BaseAgent):
    """Class for a pokemon player."""

    def __init__(self, team):
        """Initialize the agent."""
        if not team:
            raise AttributeError("Team must have at least one pokemon")

        super().__init__(type="PokemonAgent")
        self.team = team
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
        """Initialize the investment data for the opponent's team."""
        possible_combs = generate_all_ev_combinations()
        self.opp_gamestate["investment"][opp_active["name"]] = {}
        self.opp_gamestate["investment"][opp_active["name"]]["hp"] = possible_combs["hp"]
        self.opp_gamestate["investment"][opp_active["name"]]["atk"] = possible_combs["atk"]
        self.opp_gamestate["investment"][opp_active["name"]]["def"] = possible_combs["def"]
        self.opp_gamestate["investment"][opp_active["name"]]["spa"] = possible_combs["spa"]
        self.opp_gamestate["investment"][opp_active["name"]]["spd"] = possible_combs["spd"]
        self.opp_gamestate["investment"][opp_active["name"]]["spe"] = \
            generate_spe_range(opp_active["name"])

        for opp_poke in opp_team:
            self.opp_gamestate["investment"][opp_poke["name"]] = {}
            self.opp_gamestate["investment"][opp_poke["name"]]["hp"] = possible_combs["hp"]
            self.opp_gamestate["investment"][opp_poke["name"]]["atk"] = possible_combs["atk"]
            self.opp_gamestate["investment"][opp_poke["name"]]["def"] = possible_combs["def"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spa"] = possible_combs["spa"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spd"] = possible_combs["spd"]
            self.opp_gamestate["investment"][opp_poke["name"]]["spe"] = \
                generate_spe_range(opp_poke["name"])


    def update_gamestate(self, my_gamestate, opp_gamestate):
        """
        Update internal gamestate for self.

        :param my_gamestate: dict
            PokemonEngine representation of player's position.
            Should have "active" and "team" keys.
        :param opp_gamestate: dict
            PokemonEngine representation of opponent's position.
            Only % HP should be viewable, and has "active" and
            "team" keys.
        """
        self.gamestate = my_gamestate
        self.opp_gamestate["data"] = opp_gamestate

    def make_move(self):
        """
        Make a move.

        Either use random move or switch to random pokemon.
        """
        response = ()
        can_switch = len(self.gamestate["team"]) > 0

        if can_switch and uniform() < 0.5:
            switch = uniform(0, len(self.gamestate["team"]))
            switch = int(switch)
            response = "SWITCH", switch
        else:
            move = uniform(0, len(self.gamestate["active"].moves))
            move = int(move)
            response = "ATTACK", move

        return response

    def switch_faint(self):
        """
        Choose switch-in after pokemon has fainted.

        For now pick a random pokemon.
        """
        choice = uniform(0, len(self.gamestate["team"]))
        choice = int(choice)
        return choice

    def battle_position(self):
        """Calculate the battle position function."""
        self_component = self.calc_position()
        opp_component = self.calc_opp_position()

        return self_component / opp_component

    def calc_position(self):
        """Calculate the value for self's battle position."""
        return calc_position_helper(self.gamestate)

    def calc_opp_position(self):
        """Calculate the opponent's battle position."""
        return calc_opp_position_helper(self.opp_gamestate)

    def new_info(self, turn_info, my_id):
        """
        Get new info for opponent's game_state.

        Assumes Species Clause is in effect.

        :param turn_info: list
            What happened on that turn, who took what damage.
            Each element should be a dict.
        :param my_id: str
            Name corresponding to the "attacker" or "defender"
            values of this dict. To know which values the method
            should be looking at in turn_info.
        """
        for info in turn_info:
            if info["attacker"] == my_id:
                # We attacked, infer data about defending pokemon
                results, combinations = self.results_attacking(info)
                self.update_atk_inference(info, results, combinations)
            else:
                # Just got attacked, infer data about attacking pokemon
                results, combinations = self.results_defending(info)
                self.update_def_inference(info, results, combinations)

                # We're the defender, just learned about a move
                opp_name = self.opp_gamestate["data"]["active"]["name"]

                if opp_name not in self.opp_gamestate["moves"]:
                    self.opp_gamestate["moves"][opp_name] = []
                if info["move"] not in self.opp_gamestate["moves"][opp_name]:
                    self.opp_gamestate["moves"][opp_name].append(info["move"])

        if len(turn_info) == 2:
            self.update_speed_inference(turn_info, my_id)

    def update_speed_inference(self, turn_info, my_id):
        """Infer speed information from the turn info."""
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
        """Generate possible results for when we are attacking."""
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
        """Generate possible results for when we are defending."""
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
        """Decide which of potential the potential results are valid given damage dealt."""
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
            if dmg_pct >= result[0] and dmg_pct <= result[1]:
                result_dict = {}
                result_dict[stat] = {}
                result_dict["hp"] = {}
                result_dict[stat]["max_evs"] = combinations[result_ind][0]
                result_dict[stat]["positive_nature"] = combinations[result_ind][1]
                result_dict["hp"]["max_evs"] = combinations[result_ind][2]
                valid_results.append(result_dict)

        return valid_results

    def valid_results_def(self, poke_name, stat, dmg_pct, results, combinations):
        """Decide which of potential the potential results are valid given damage dealt."""
        valid_results = []
        num_results = len(results)

        if poke_name not in self.opp_gamestate["investment"]:
            self.opp_gamestate["investment"][poke_name] = {}

        if stat not in self.opp_gamestate["investment"][poke_name]:
            self.opp_gamestate["investment"][poke_name][stat] = []

        for result_ind in range(num_results):
            result = results[result_ind]
            if dmg_pct >= result[0] and dmg_pct <= result[1]:
                result_dict = {}
                result_dict["max_evs"] = combinations[result_ind][0]
                result_dict["positive_nature"] = combinations[result_ind][1]
                valid_results.append(result_dict)

        return valid_results

    def update_atk_inference(self, turn_info, results, combinations):
        """Update the opponent's defense investment information."""
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

    def update_def_inference(self, turn_info, results, combinations):
        """Update the opponent's attack investment information."""
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

def battle_position_helper(player_gs, opp_gs):
    """Calculate the battle position for generic gamestates."""
    self_component = calc_position_helper(player_gs)
    opp_component = calc_opp_position_helper(opp_gs)

    return (self_component+0.01) / (opp_component+0.01)

def calc_position_helper(player_gs):
    """Calculate the player's gamestate value."""
    my_posn = 0
    active_poke = player_gs["active"]
    if active_poke is not None and active_poke.current_hp > 0:
        my_posn += active_poke.current_hp / active_poke.max_hp

    for poke in player_gs["team"] and poke.current_hp > 0:
        my_posn += poke.current_hp / poke.max_hp

    return my_posn

def calc_opp_position_helper(opp_gs):
    """Calculate the player's opponent's gamestate value."""
    opp_posn = 0
    active_poke = opp_gs["data"]["active"]
    if active_poke is not None and active_poke["pct_hp"] > 0:
        opp_posn += active_poke["pct_hp"]

    for poke in opp_gs["data"]["team"]:
        if poke["pct_hp"] > 0:
            opp_posn += poke["pct_hp"]

    return opp_posn

def generate_all_ev_combinations():
    """Generate all possible stat investment combinations."""
    combinations = {}

    combinations["atk"] = []
    combinations["spa"] = []
    atk_combinations = []
    atk_combinations.append((False, False))
    atk_combinations.append((True, False))
    atk_combinations.append((False, True))
    atk_combinations.append((True, True))
    for combination in atk_combinations:
        result_dict = {}
        result_dict["max_evs"] = combination[0]
        result_dict["positive_nature"] = combination[1]
        combinations["atk"].append(result_dict)
        combinations["spa"].append(result_dict)

    combinations["hp"] = []
    combinations["def"] = []
    combinations["spd"] = []

    def_combinations = []
    def_combinations.append((False, False))
    def_combinations.append((False, False))
    def_combinations.append((True, False))
    def_combinations.append((True, False))
    def_combinations.append((False, True))
    def_combinations.append((False, True))
    def_combinations.append((True, True))
    def_combinations.append((True, True))

    for combination in def_combinations:
        result_dict = {}
        result_dict["max_evs"] = combination[0]
        result_dict["positive_nature"] = combination[1]
        combinations["def"].append(result_dict)
        combinations["spd"].append(result_dict)

    combinations["hp"].append({"max_evs": True})
    combinations["hp"].append({"max_evs": False})

    return combinations

def generate_spe_range(pokemon_name):
    """Calculate the range for a pokemon's speed."""
    # Slowest possible opponent's pokemon
    min_speed = Pokemon(name=pokemon_name, moves=["tackle"], nature="brave").speed
    # Fastest possible opponent's pokemon
    max_speed = Pokemon(name=pokemon_name,
                        moves=["tackle"],
                        evs={"spe": 252},
                        nature="jolly").speed
    return [min_speed, max_speed]
