"""Module for Pokemon Helpers calculations."""

from math import floor
from random import uniform
from random import random

from config import POKEMON_DATA
from config import WEAKNESS_CHART
from config import (BRN_STATUS, PSN_STATUS, TOX_STATUS)


def calculate_stat(base_val, ev_val, level):
    """
    Calculate the value for a given pokemon statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats

    Args:
        base_val (int): The pokemon's base statistic value in that statistic.
        ev_val (int): The pokemon's effort values in that statistic
        level (int): Pokemon's level

    Returns:
        Value for the statistic

    """
    stat_val = floor((2*(base_val) + 31 + floor(ev_val/4))*level/100)
    stat_val += 5
    return stat_val


def calculate_hp_stat(base_hp, ev_val, level):
    """
    Calculate the value for a pokemon's Hit Points statistic.

    Formula from
        https://bulbapedia.bulbagarden.net/wiki/Statistic#Determination_of_stats

    Args:
        base_hp (int): Base HP statistic.
        ev_val (int): Pokemon's effort values in hitpoints.
        level (int): Pokemon's level

    Returns:
        Maximum hitpoints for the pokemon.

    """
    hp_val = floor((2*base_hp + 31 + floor(ev_val/4))*level/100)
    hp_val += level + 10
    return hp_val


def calculate_spe_range(pokemon_name):
    """
    Calculate the range for a pokemon's speed.

    Args:
        pokmeon_name (str): The name of the pokemon for whom the range is being calculated.

    Returns:
        Tuple win min/max speed for this Pokemon

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


def calc_boost_factor(pokemon, stat_name):
    """
    Calculate the multiplicative modifier for a pokemon's stat.

    Args:
        pokemon (Pokemon): The pokemon for whom we are calculating.
        stat (str): The stat for which we are calculating this for.

    Returns:
        The multiplier to apply to that pokemon's stat.

    """
    return max(2, 2 + pokemon["boosts"][stat_name]) / \
        max(2, 2 - pokemon["boosts"][stat_name])


def calculate_status_damage(pokemon):
    """
    Calculate the % HP to remove as status damage.

    Args:
        pokemon (Pokemon or dict): The pokemon that this damage is calculated for.
            pokemon.status is None if no status, otherwise one of the _STATUS
            variables in the config.

    Returns:
        Float value for the % Damage it will take from status this turn.

    """
    dmg_pct = 0
    if pokemon["status"] == BRN_STATUS:
        # Burns do 1/16 of hp
        dmg_pct = 1.0/16
    elif pokemon["status"] == PSN_STATUS:
        # Poison does 1/8 of hp
        dmg_pct = 1.0/8
    elif pokemon["status"] == TOX_STATUS:
        # Toxic does variable damage
        dmg_pct = (pokemon["status_turns"]+1)*1.0/16

    return dmg_pct


def calculate_modifier(move, attacker, defender):
    """
    Calculate the damage modifier for an attack.

    Factors in STAB, and type effectiveness.

    Args:
        move (dict): Information on the move being used.
        attacker (Pokemon): The pokemon using the attack.
        defender (Pokemon): The pokemon that is recieving the attack.

    Returns:
        The multipler to apply to the damage.

    """
    modifier = 1

    # STAB Modifier
    if move["type"] in attacker["types"]:
        modifier = modifier * 1.5

    # Weakness modifier
    for def_type in defender["types"]:
        if move["type"] in WEAKNESS_CHART[def_type]:
            modifier = modifier * WEAKNESS_CHART[def_type][move["type"]]

    return modifier


def calculate_damage(move, attacker, defender):
    """
    Calculate damage of a move.

    Args:
        move (dict): Information on the move being used.
        attacker (Pokemon): The pokemon using the attack.
        defender (Pokemon): The pokemon that is recieving the attack.

    Returns:
        The damage dealt by this move, as well as a flag whether or not
            the attack resulted in a critical hit.

    """
    damage = 0
    critical_hit = False
    # Status moves do no damage
    if move["category"] == "Status":
        return damage, critical_hit

    # Calculate actual damage
    damage = floor(2*attacker["level"]/5 + 2)
    damage = damage * move["basePower"]
    if move["category"] == "Physical":
        damage = floor(damage * attacker.effective_stat("atk")) / \
            defender.effective_stat("def")
    elif move["category"] == "Special":
        damage = floor(damage * attacker.effective_stat("spa")) / \
            defender.effective_stat("spd")
    damage = floor(damage/50) + 2

    # Damage Modifier
    modifier = calculate_modifier(move, attacker, defender)

    # Critical Hit
    if random() < 0.0625:
        critical_hit = True
        modifier = modifier * 1.5

    # Random Damage range
    modifier = modifier * uniform(0.85, 1.00)
    damage = floor(damage*modifier)

    return (damage, critical_hit)
