"""Class for a pokemon used by a PokemonAgent."""

from math import floor

from config import MOVE_DATA
from config import POKEMON_DATA
from config import NATURES


class Pokemon:
    """The pokemon class."""

    # pylint: disable=too-many-instance-attributes
    # Packaging values as a dictionary is kind of pointless
    def __init__(self, name, moves, level=100, nature="quirky", evs={}):
        """
        Initialize a pokemon.

        Make a new instance of species <name> with moves <moves>
        at level <level> with nature <quirky>

        :param name: str
            String corresponding to value in config.POKEMON_DATA
        :param moves: list
            List of moves corresponding to moves in config.MOVE_DATA
        :param level: int
            Level of pokemon to be used in calculations
        :param nature: str
            Pokemon nature to be used to modify stat values.
        :param evs: dict
            Dictionary of key/value pairs with EVs for each stat.
            Key should be stat code, value should be number of EVs.
        """
        # Validate pokemon chosen
        if name not in POKEMON_DATA:
            raise AttributeError("Invalid pokemon chosen: {}.".format(name))

        # Validate moves
        if not moves:
            raise AttributeError("Moves must be provided.")
        for move in moves:
            if move not in MOVE_DATA:
                raise AttributeError("Invalid move chosen: {}.".format(move))

        # Validate level
        if level not in range(1, 101):
            raise AttributeError("Level must be between 1 and 100")

        # Validate nature
        if nature not in NATURES:
            raise AttributeError("Invalid nature chosen: {}".format(nature))

        self.name = name
        self.level = level
        self.moves = []
        for move in moves:
            self.moves.append(MOVE_DATA[move])
        self.types = POKEMON_DATA[self.name]["types"]
        self.set_stats(nature)

    def set_stats(self, nature):
        """
        Calculate stats for the pokemon.

        :param nature: str
            Nature of the pokemon to modify stats.
        """
        base_stats = POKEMON_DATA[self.name]["baseStats"]

        # Calculate the statistic values
        self.max_hp = calculate_hp_stat(base_stats["hp"], self.level)
        self.current_hp = self.max_hp
        self.attack = calculate_stat(base_stats["atk"], self.level)
        self.defense = calculate_stat(base_stats["def"], self.level)
        self.sp_attack = calculate_stat(base_stats["spa"], self.level)
        self.sp_defense = calculate_stat(base_stats["spd"], self.level)
        self.speed = calculate_stat(base_stats["spe"], self.level)

        # Update with nature modifiers
        if NATURES[nature]["increase"] is not None:
            increase_stat = NATURES[nature]["increase"]
            decrease_stat = NATURES[nature]["decrease"]
            mod_inc = floor(self.__getattribute__(increase_stat)*1.1)
            mod_dec = floor(self.__getattribute__(decrease_stat)*0.9)
            self.__setattr__(increase_stat, mod_inc)
            self.__setattr__(decrease_stat, mod_dec)


def calculate_stat(base_val, level):
    """
    Calculate the value for a given pokemon statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats_2

    :param base_val: int
        The pokemon's base statistic value in that statistic
    :param level: int
        The pokemon's level
    """
    return floor(2*base_val*level/100) + 5


def calculate_hp_stat(base_hp, level):
    """
    Calculate the value for a pokemon's Hit Points statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats_2

    :param base_hp: int
        The pokemon's base HP statistic
    :param level: int
        The pokemon's level
    """
    hp_val = floor(2*base_hp*level/100)
    hp_val += level + 10
    return hp_val
