"""Class for a pokemon player."""

from random import random
from random import uniform
import logging

from agent.base_agent import BaseAgent
from pokemon_helpers.damage_stats import DamageStatCalc
from pokemon_helpers.pkmn_player_gamestate import PokemonPlayerGameState


class PokemonAgent(BaseAgent):
    """
    Class for a pokemon player.

    Attributes:
        team (list): The team of pokemon this agent uses.
        gamestate (dict): This player's internal representation of a game.
        opp_gamestate (dict): This player's knowledge about the opponent's team in this game.
        dmg_stat_calc (DamageStatCalc): The class to do estimate damage using Damage Stats.

    """

    def __init__(self, team):
        """Initialize the agent."""
        if not team:
            raise AttributeError("Team must have at least one pokemon")

        super().__init__(type="PokemonAgent")
        self.team = team
        self.game_state = PokemonPlayerGameState()
        self.dmg_stat_calc = DamageStatCalc()

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.game_state.reset_gamestates()

    def init_opp_gamestate(self, opp_team, opp_active):
        """
        Initialize the investment data for the opponent's team.

        Args:
            opp_team (list): List with the opponent's Pokemon.
            opp_active (Pokemon): Opponent's active Pokemon.

        """
        self.game_state.init_opp_gamestate(opp_team, opp_active)

    def update_gamestate(self, my_gamestate, opp_gamestate):
        """
        Update internal gamestate for self.

        Args:
            my_gamestate (dict): PokemonEngine representation of player's position.
                Should have "active" and "team" keys.
            opp_gamestate (dict): PokemonEngine representation of opponent's position.
                Only % HP should be viewable, and has "active" and "team" keys.

        """
        self.game_state.update_gamestate(my_gamestate, opp_gamestate)

    def _num_remaining_pokemon(self):
        """Returns the number of pokemon who have not yet fainted."""
        return len(self.game_state.gamestate["team"])

    def make_move(self):
        """
        Make a move.

        Either use random move or switch to random pokemon.

        Returns:
            Tuple with move type (ATTACK or SWITCH and the position.

        """
        response = ()
        active_can_switch, moves = self.game_state.gamestate["active"].possible_moves()
        can_switch = self._num_remaining_pokemon() > 0 and active_can_switch

        logging.info("PokemonAgent:make_move:%s:can_switch:%s",
                     self.id, can_switch)

        if can_switch and random() < 0.5:
            switch = int(uniform(0, self._num_remaining_pokemon()))
            response = "SWITCH", switch
        else:
            move_ind = int(uniform(0, len(moves)))
            response = moves[move_ind]

        logging.info("PokemonAgent:make_move:%s:chosen_move:%s",
                     self.id, response)

        return response

    def switch_faint(self):
        """
        Choose switch-in after pokemon has fainted.

        For now pick a random pokemon.

        Returns:
            Position of the next pokemon to switch to.

        """
        if not self._num_remaining_pokemon():
            raise RuntimeError("No members left, cannot switch")

        choice = uniform(0, self._num_remaining_pokemon())
        choice = int(choice)

        logging.info("PokemonAgent:switch_faint:%s:num_remaining_pkmn:%s",
                     self.id, self._num_remaining_pokemon())
        logging.info("PokemonAgent:switch_faint:%s:switch_to:%s",
                     self.id, choice)

        return choice

    def battle_position(self):
        """
        Calculate the battle position function.

        Returns:
            This player's current % HP divided by the
                Opponent's current % HP.

        """
        self_component = self.calc_position()
        opp_component = self.calc_opp_position()
        final_position = self_component / opp_component

        logging.info("PokemonAgent:battle_position:%s:self_component:%s",
                     self.id, self_component)
        logging.info("PokemonAgent:battle_position:%s:opp_component:%s",
                     self.id, opp_component)
        logging.info("PokemonAgent:battle_position:%s:battle_position:%s",
                     self.id, final_position)

        return final_position

    def calc_position(self):
        """
        Calculate the value for self's battle position.

        Returns:
            This player's remaining % HP.

        """
        # TODO: Make this a private function
        return calc_position_helper(self.game_state.gamestate)

    def calc_opp_position(self):
        """
        Calculate the opponent's battle position.

        Returns:
            The opponent's remaining % HP.

        """
        # TODO: Make this a private function
        return calc_opp_position_helper(self.game_state.opp_gamestate)

    def new_info(self, raw_turn_info):
        """
        Get new info for opponent's game_state.

        Assumes Species Clause is in effect.

        Args:
            turn_info (list): What happened on that turn, who took what damage.
            my_id (str): Name corresponding to the "attacker" or "defender"
                values of this dict. To know which values the method
                should be looking at in turn_info.
        """
        self.game_state.new_info(raw_turn_info, self.id)


def battle_position_helper(player_gs, opp_gs):
    """
    Calculate the battle position for generic gamestates.

    Args:
        player_gs (dict): Dictionary representation of player gamestate.
        opp_gs (dict): Dictionary representation of opponent's gamestate.

    Returns:
        Player's battle position divided by opponent's battle position.

    """
    self_component = calc_position_helper(player_gs)
    opp_component = calc_opp_position_helper(opp_gs)

    return (self_component+0.01) / (opp_component+0.01)


def calc_position_helper(player_gs):
    """
    Calculate the player's gamestate value.

    Args:
        player_gs (dict): Dictionary representation of player gamestate.

    Returns:
        The player's battle position value.
            Calculated as percent remaining hit points.

    """
    my_posn = 0
    active_poke = player_gs["active"]
    if active_poke is not None and active_poke.current_hp > 0:
        my_posn += active_poke.current_hp / active_poke.max_hp

    for poke in player_gs["team"]:
        if poke.current_hp > 0:
            my_posn += poke.current_hp / poke.max_hp

    return my_posn


def calc_opp_position_helper(opp_gs):
    """
    Calculate the player's opponent's gamestate value.

    Args:
        opp_gs (dict): Dictionary representation of the opponent's gamestate.

    Returns:
        The opponent's battle position value.
            Calculated as percent remaining hit points.

    """
    opp_posn = 0
    active_poke = opp_gs["data"]["active"]
    if active_poke is not None and active_poke["pct_hp"] > 0:
        opp_posn += active_poke["pct_hp"]

    for poke in opp_gs["data"]["team"]:
        if poke["pct_hp"] > 0:
            opp_posn += poke["pct_hp"]

    return opp_posn
