"""Class defining an Engine's Game State."""

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


    def __getitem__(self, key):
        """
        Define [] lookup on this object.

        :param key: str
            Attribute of this object to get.
        """
        return self.__getattribute__(key)
