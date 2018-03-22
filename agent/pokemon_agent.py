"""Class for a pokemon player."""

from numpy.random import uniform
from agent.base_agent import BaseAgent
from pokemon.damage_stats import DamageStatCalc

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
        my_posn = 0
        active_poke = self.gamestate["active"]
        if active_poke is not None:
            my_posn += active_poke.current_hp / active_poke.max_hp

        for poke in self.gamestate["team"]:
            my_posn += poke.current_hp / poke.max_hp

        return my_posn

    def calc_opp_position(self):
        """Calculate the opponent's battle position."""
        opp_posn = 0
        active_poke = self.opp_gamestate["data"]["active"]
        if active_poke is not None:
            opp_posn += active_poke["pct_hp"]

        for poke in self.opp_gamestate["data"]["team"]:
            opp_posn += poke["pct_hp"]

        return opp_posn

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
