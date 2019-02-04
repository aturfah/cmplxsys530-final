"""Classes defining Pokemon moves."""


class BaseMove:
    """Base class for all moves."""

    # pylint: disable=R0902
    # I need all these attributes.

    def __init__(self, **kwargs):
        """
        Initialize a move.

        Arguments are defined by config.
        """
        # pylint: disable=R0915
        # I need to define these arguments
        self.is_viable = kwargs.get("isViable")
        self.on_base_power_priority = kwargs.get("onBasePowerPriority")
        self.id = kwargs.get("id") #  pylint: disable=C0103
        self.num = kwargs.get("num")
        self._self = kwargs.get("self")
        self.recoil = kwargs.get("recoil")
        self.no_sketch = kwargs.get("noSketch")
        self.is_future_move = kwargs.get("isFutureMove")
        self.side_condition = kwargs.get("sideCondition")
        self.secondary = kwargs.get("secondary")
        self.power_points = kwargs.get("pp")
        self.thaws_target = kwargs.get("thawsTarget")
        self.z_move_effect = kwargs.get("zMoveEffect")
        if self.z_move_effect is None:
            self.z_move_effect = kwargs.get("zmoveEffect")
        self.effect = kwargs.get("effect")
        self.ignore_defensive = kwargs.get("ignoreDefensive")
        self.use_target_offensive = kwargs.get("useTargetOffensive")
        self.sleep_usable = kwargs.get("sleepUsable")
        self.name = kwargs.get("name")
        self.status = kwargs.get("status")
        self.terrain = kwargs.get("terrain")
        self.weather = kwargs.get("weather")
        self.multihit = kwargs.get("multihit")
        self.pressure_target = kwargs.get("pressureTarget")
        self.np_pp_boosts = kwargs.get("noPPBoosts")
        self.on_before_move_priority = kwargs.get("onBeforeMovePriority")
        self.is_nonstandard = kwargs.get("isNonstandard")
        self.ignore_evasion = kwargs.get("ignoreEvasion")
        self.non_ghost_target = kwargs.get("nonGhostTarget")
        self.no_faint = kwargs.get("noFaint")
        self.category = kwargs.get("category")
        self.stalling_move = kwargs.get("stallingMove")
        self.multiaccuracy = kwargs.get("multiaccuracy")
        self.crit_ratio = kwargs.get("critRatio")
        self.defensive_category = kwargs.get("defensiveCategory")
        self.z_move_power = kwargs.get("zMovePower")
        self.on_try_hit = kwargs.get("onTryHit")
        self.self_destruct = kwargs.get("selfdestruct")
        self.ignore_ability = kwargs.get("ignoreAbility")
        self.mind_blown_recoil = kwargs.get("mindBlownRecoil")
        self.z_move_boost = kwargs.get("zMoveBoost")
        self.type = kwargs.get("type")
        self.breaks_protect = kwargs.get("breaksProtect")
        self.struggle_recoil = kwargs.get("struggleRecoil")
        self.has_custom_recoil = kwargs.get("hasCustomRecoil")
        self.ignore_immunity = kwargs.get("ignoreImmunity")
        self.is_unreleased = kwargs.get("isUnreleased")
        self.no_metrenome = kwargs.get("noMetrenome")
        self.self_switch = kwargs.get("selfSwitch")
        self.heal = kwargs.get("heal")
        self.steals_boosts = kwargs.get("stealsBoosts")
        self.desc = kwargs.get("desc")
        self.accuracy = kwargs.get("accuracy")
        self.damage = kwargs.get("damage")
        self.volatile_status = kwargs.get("volatileStatus")
        self.ohko = kwargs.get("ohko")
        self.force_switch = kwargs.get("forceSwitch")
        self.pseudo_weather = kwargs.get("pseudoWeather")
        self.base_power = kwargs.get("basePower")
        self.secondaries = kwargs.get("secondaries")
        self.is_z = kwargs.get("isZ")
        self.self_boost = kwargs.get("selfBoost")

    def get(self, key, default=None):
        """
        Extend __getitem__ to have defaults.

        Args:
            key (str): Attribute of this object to get.
            default: What to return if there is no such key.

        Returns:
            Value of this object's key, if it exists. If not, return value
                specified in default.

        """
        if self.__contains__(key):
            return self.__getitem__(key)

        return default

    def __contains__(self, key):
        """
        Define 'in' operator on this object.

        Args:
            key (str): Attribute to theck this object for.

        Returns:
            True if this object has 'key' as an attribute.

        """
        try:
            self.__getattribute__(key)
        except AttributeError:
            return False

        return True

    def __getitem__(self, key):
        """
        Define [] operating on this object.

        Args:
            key (str): Attribute of this object to get.

        Returns:
            Value of this object's key.

        """
        if key == "baseStats":
            key = "base_stats"
        return self.__getattribute__(key)
