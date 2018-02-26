"""Class for a pokemon player."""

from agent.base_agent import BaseAgent

class PokemonAgent(BaseAgent):
    """Class for a pokemon player."""
    
    def __init__(self, team):
        """Initialize the agent."""
        super().__init__(type="PokemonAgent")
        self.team = team
        self.gamestate = None
    
