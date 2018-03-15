"""
Class for calculating damage stats for a pokemon.

Based on https://www.smogon.com/smog/issue4/damage_stats
"""

from math import inf
from math import ceil, floor

from battle_engine.pokemon_engine import calculate_modifier

class DamageStatCalc():
    """The class to do the thing."""

    def __init__(self):
        """Initialize the calculator."""
        self.damage_stats = {}
        self.build_stats()

    def calculate_range(self, move, attacker, defender, params):
        """
        Calculate the damage range for a player's attack.
        :param attacker: dict
            Stats and boosts for the attacking pokemon.
        :param defender: dict
            Stats and boosts for the defending pokemon.
        :param move: dict
            Dictionary with the move's data.
        :param params: dict
            Dictionary with three required keys, 'atk' and
            'def', and 'hp' with the kwargs for the estimate_dmg_val
            calculations.
        """
        move_cat = ("atk", "def")
        if move["category"] != "Physical":
            move_cat = ("spa", "spd")

        atk_params = params["atk"]
        def_params = params["def"]
        hp_params = params["hp"]

        modifier = calculate_modifier(move, attacker, defender)
        d_atk = self.estimate_dmg_val(attacker["baseStats"][move_cat[0]], is_atk=True, **atk_params)
        d_hp = self.estimate_dmg_val(defender["baseStats"]["hp"], is_hp=True, **hp_params)
        d_def = self.estimate_dmg_val(defender["baseStats"][move_cat[1]], **def_params)


        max_dmg = d_atk * modifier * move["basePower"]
        max_dmg = max_dmg / (d_hp * d_def)

        # Ceiling so we get a conservative estimate
        return (0.85*floor(max_dmg), ceil(max_dmg))

    def estimate_dmg_val(self, stat_val, **kwargs):
        """Estimate the value of a damage_statistic."""
        is_hp = kwargs.get("is_hp", False)
        is_atk = kwargs.get("is_atk", False)
        max_evs = kwargs.get("max_evs", False)
        positive_nature = kwargs.get("positive_nature", False)

        dmg_val = None
        if stat_val in self.damage_stats:
            dmg_val = self.damage_stats[stat_val]
        else:
            closest_num, offset = self.find_closest_level(stat_val)
            dmg_val = self.damage_stats[closest_num]
            dmg_val += 0.19*offset/2

        if is_hp:
            dmg_val = dmg_val + 5
        elif is_atk:
            if max_evs:
                dmg_val += 3

            dmg_val = dmg_val * 4

        if positive_nature:
            dmg_val *= 1.1

        # Hacky way to get around the .499999
        # not rounding properly.
        dmg_val = round(round(dmg_val, 3), 2)

        return dmg_val

    def find_closest_level(self, number):
        """
        Find the closest value in the keys to this number.

        Rounds down, so 215 mathces to 200.
        """
        closest_num = None
        offset = None
        values = list(self.damage_stats.keys())

        if number < values[0]:
            return values[0], number - values[0]

        differences = [number - val for val in values]

        smallest_diff_ind = None
        smallest_diff = inf
        index = 0
        for diff in differences:
            if abs(diff) < smallest_diff:
                smallest_diff = diff
                smallest_diff_ind = index
            index += 1

        closest_num = values[smallest_diff_ind]
        offset = smallest_diff

        return closest_num, offset

    def build_stats(self):
        """Build the dictionary for the stat numbers."""
        self.damage_stats[5] = 2.19
        self.damage_stats[10] = 2.67
        self.damage_stats[15] = 3.14
        self.damage_stats[20] = 3.62
        self.damage_stats[25] = 4.10
        self.damage_stats[30] = 4.57
        self.damage_stats[35] = 5.05
        self.damage_stats[40] = 5.52
        self.damage_stats[45] = 6.00
        self.damage_stats[50] = 6.48
        self.damage_stats[55] = 6.95
        self.damage_stats[60] = 7.43
        self.damage_stats[65] = 7.90
        self.damage_stats[70] = 8.38
        self.damage_stats[75] = 8.86
        self.damage_stats[80] = 9.33
        self.damage_stats[85] = 9.81
        self.damage_stats[90] = 10.29
        self.damage_stats[95] = 10.76
        self.damage_stats[100] = 11.24
        self.damage_stats[105] = 11.71
        self.damage_stats[110] = 12.19
        self.damage_stats[115] = 12.67
        self.damage_stats[120] = 13.14
        self.damage_stats[125] = 13.62
        self.damage_stats[130] = 14.10
        self.damage_stats[135] = 14.57
        self.damage_stats[140] = 15.05
        self.damage_stats[145] = 15.52
        self.damage_stats[150] = 16.00
        self.damage_stats[160] = 16.95
        self.damage_stats[165] = 17.43
        self.damage_stats[170] = 17.90
        self.damage_stats[180] = 18.86
        self.damage_stats[190] = 19.81
        self.damage_stats[200] = 20.76
        self.damage_stats[230] = 23.62
        self.damage_stats[250] = 25.52
        self.damage_stats[255] = 260
