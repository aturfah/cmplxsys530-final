"""Class for a pokemon player."""

from numpy.random import uniform
from agent.base_agent import BaseAgent
from pokemon.damage_stats import DamageStatCalc


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
        self.dmg_stat_calc = DamageStatCalc()

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.gamestate = {}
        self.opp_gamestate = {}
        self.opp_gamestate["data"] = {}
        self.opp_gamestate["moves"] = {}

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
                # We're the attacker
                pass
            else:
                # We're the defender, just learned about a move
                opp_name = self.opp_gamestate["data"]["active"]["name"]

                if opp_name not in self.opp_gamestate["moves"]:
                    self.opp_gamestate["moves"][opp_name] = []
                if info["move"] not in self.opp_gamestate["moves"][opp_name]:
                    self.opp_gamestate["moves"][opp_name].append(info["move"])

    def make_move(self):
        """
        Make a move.

        Either use random move or switch to first pokemon.
        """
        response = ()
        can_switch = len(self.gamestate["team"]) > 0

        if can_switch and uniform() < 0.5:
            response = "SWITCH", 0
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
