"""Class for a pokemon used by a PokemonAgent."""

from math import floor

from config import MOVE_DATA
from config import POKEMON_DATA

NATURES = {
    "hardy": {
        "increase": None,
        "decrease": None
    },
    "lonely": {
        "increase": "attack",
        "decrease": "defense"
    },
    "brave": {
        "increase": "attack",
        "decrease": "speed"
    },
    "adamant": {
        "increase": "attack",
        "decrease": "sp_attack"
    },
    "naughty": {
        "increase": "attack",
        "decrease": "sp_defense"
    },
    "bold": {
        "increase": "defense",
        "decrease": "attack"
    },
    "docile": {
        "increase": None,
        "decrease": None
    },
    "relaxed": {
        "increase": "defense",
        "decrease": "speed"
    },
    "impish": {
        "increase": "defense",
        "decrease": "sp_attack"
    },
    "lax": {
        "increase": "defense",
        "decrease": "sp_defense"
    },
    "timid": {
        "increase": "speed",
        "decrease": "attack"
    },
    "hasty": {
        "increase": "speed",
        "decrease": "defense"
    },
    "serious": {
        "increase": None,
        "decrease": None
    },
    "jolly": {
        "increase": "speed",
        "decrease": "sp_attack"
    },
    "naive": {
        "increase": "speed",
        "decrease": "sp_defense"
    },
    "modest": {
        "increase": "sp_attack",
        "decrease": "attack"
    },
    "quiet": {
        "increase": "sp_attack",
        "decrease": "speed"
    },
    "mild": {
        "increase": "sp_attack",
        "decrease": "defense"
    },
    "bashful": {
        "increase": None,
        "decrease": None
    },
    "rash": {
        "increase": "sp_attack",
        "decrease": "sp_defense"
    },
    "Calm": {
        "increase": "sp_defense",
        "decrease": "attack"
    },
    "gentle": {
        "increase": "sp_defense",
        "decrease": "defense"
    },
    "sassy": {
        "increase": "sp_defense",
        "decrease": "speed"
    },
    "careful": {
        "increase": "sp_defense",
        "decrease": "sp_attack"
    },
    "quirky": {
        "increase": None,
        "decrease": None
    }
}


class Pokemon:
    """The pokemon class."""

    def __init__(self, name, moves, level=100, nature="quirky"):
        """Initialize a pokemon."""
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
        self.nature = nature
        self.moves = {}
        for move in moves:
            self.moves[move] = MOVE_DATA[move]

        self.set_stats()

    def set_stats(self):
        """Calculate stats for the pokemon."""
        base_stats = POKEMON_DATA[self.name]["baseStats"]

        # Calculate the statistic values
        self.max_hp = calculate_hp_stat(base_stats["hp"], self.level)
        self.attack = calculate_stat(base_stats["atk"], self.level)
        self.defense = calculate_stat(base_stats["def"], self.level)
        self.sp_attack = calculate_stat(base_stats["spa"], self.level)
        self.sp_defense = calculate_stat(base_stats["spd"], self.level)
        self.speed = calculate_stat(base_stats["spe"], self.level)

        # Update with nature modifiers
        if NATURES[self.nature]["increase"] is not None:
            increase_stat = NATURES[self.nature]["increase"]
            decrease_stat = NATURES[self.nature]["decrease"]
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
