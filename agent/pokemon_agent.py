"""Class for a pokemon player."""

from numpy.random import uniform
from agent.base_agent import BaseAgent


class PokemonAgent(BaseAgent):
    """Class for a pokemon player."""

    def __init__(self, team):
        """Initialize the agent."""
        if not team:
            raise AttributeError("Team must have at least one pokemon")

        super().__init__(type="PokemonAgent")
        self.team = team
        self.gamestate = None
        self.opp_gamestate = None

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.gamestate = None
        self.opp_gamestate = None

    def update_gamestate(self, my_gamestate, opp_gamestate):
        """Update internal gamestate for self."""
        self.gamestate = my_gamestate
        self.opp_gamestate = opp_gamestate

    def new_info(self, turn_info, my_id):
        """Get new info for opponent's game_state."""
        for info in turn_info:
            if info["attacker"] == my_id:
                # We're the attacker
                pass
            else:
                # We're the defender, just learned about a move
                pass

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
