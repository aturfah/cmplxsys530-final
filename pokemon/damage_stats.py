"""
Class for calculating damage stats for a pokemon.

Based on https://www.smogon.com/smog/issue4/damage_stats
"""

class DamageStatCalc():
    """The class to do the thing."""

    def __init__(self):
        """Initialize the calculator."""
        self.damage_stats = {}
    
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

    def estimate_dmg_val(self, stat_val, is_hp = False, is_atk = False, max_evs = False):
        """Estimate the value of a damage_statistic."""
        dmg_val = None
        if stat_val in self.damage_stats:
            dmg_val = self.damage_stats[stat_val]
        else:
            # IMPLEMENT ME LATER
            pass
        
        if is_hp:
            dmg_val = dmg_val + 5
        elif is_atk:
            if max_evs:
                dmg_val += 3

            dmg_val = dmg_val * 4

        return dmg_val
