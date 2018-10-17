"""Module for Pokemon Helpers calculations."""

from math import floor

from config import POKEMON_DATA


def calculate_stat(base_val, ev_val, level):
    """
    Calculate the value for a given pokemon statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats

    :param base_val: int
        The pokemon's base statistic value in that statistic
    :param ev_val: int
        The pokemon's effort values in that statistic
    :param level: int
        The pokemon's level
    """
    stat_val = floor((2*(base_val) + 31 + floor(ev_val/4))*level/100)
    stat_val += 5
    return stat_val


def calculate_hp_stat(base_hp, ev_val, level):
    """
    Calculate the value for a pokemon's Hit Points statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats

    :param base_hp: int
        The pokemon's base HP statistic
    :param ev_val: int
        The pokemon's effort values in hitpoints statistic
    :param level: int
        The pokemon's level
    """
    hp_val = floor((2*base_hp + 31 + floor(ev_val/4))*level/100)
    hp_val += level + 10
    return hp_val


def calculate_spe_range(pokemon_name):
    """
    Calculate the range for a pokemon's speed.

    :param pokemon_name: str
        The name of the pokemon for whom the range is being calculated.
    """
    speed_base_stat = POKEMON_DATA[pokemon_name]["baseStats"]["spe"]

    # Slowest possible opponent's pokemon
    min_speed = calculate_stat(speed_base_stat, 0, 100)*0.9

    # Fastest possible opponent's pokemon
    max_speed = calculate_stat(speed_base_stat, 252, 100)*1.1

    return [min_speed, max_speed]


def generate_all_ev_combinations():
    """Generate all possible stat investment combinations."""
    combinations = {}

    combinations["atk"] = []
    combinations["spa"] = []
    atk_combinations = []
    atk_combinations.append((False, False))
    atk_combinations.append((True, False))
    atk_combinations.append((False, True))
    atk_combinations.append((True, True))
    for combination in atk_combinations:
        result_dict = {}
        result_dict["max_evs"] = combination[0]
        result_dict["positive_nature"] = combination[1]
        combinations["atk"].append(result_dict)
        combinations["spa"].append(result_dict)

    combinations["hp"] = []
    combinations["def"] = []
    combinations["spd"] = []

    def_combinations = []
    def_combinations.append((False, False))
    def_combinations.append((True, False))
    def_combinations.append((False, True))
    def_combinations.append((True, True))

    for combination in def_combinations:
        result_dict = {}
        result_dict["max_evs"] = combination[0]
        result_dict["positive_nature"] = combination[1]
        combinations["def"].append(result_dict)
        combinations["spd"].append(result_dict)

    combinations["hp"].append({"max_evs": True})
    combinations["hp"].append({"max_evs": False})

    return combinations
