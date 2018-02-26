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
        self.gamestate = None

    def make_move(self):
        """Make a move. For now just use first move."""
        return "ATTACK", 1
