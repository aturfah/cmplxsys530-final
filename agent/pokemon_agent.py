"""Class for a pokemon player."""

from agent.base_agent import BaseAgent

class PokemonAgent(BaseAgent):
    """Class for a pokemon player."""
    
    def __init__(self, team):
        """Initialize the agent."""
        if not team:
            raise AttributeError("Team must have at least one pokemon")

        super().__init__(type="PokemonAgent")
        self.team = team
        self.reset_gamestates()

    def reset_gamestates(self):
        """Reset gamestate values for a new battle."""
        self.gamestate = None
        self.opp_gamestate = None

    self.update_gamestate(self, new_gamestate):
        """Update internal gamestate for self."""
        self.gamestate = new_gamestate

    def make_move(self, my_gamestate=None):
        """Make a move. For now just use first move."""
        return "ATTACK", 1
