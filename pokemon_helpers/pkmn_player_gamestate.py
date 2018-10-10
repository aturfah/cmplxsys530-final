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

    def __getitem__(self, key):
        """
        Define [] lookup on this object.

        :param key: str
            Attribute of this object to get.
        """
        return self.__getattribute__(key)
