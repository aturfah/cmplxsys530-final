"""Classes defining Pokemon moves."""

from math import floor
from random import uniform
from random import random

from config import WEAKNESS_CHART, STATUS_IMMUNITIES


class BaseMove():
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
        self.flags = kwargs.get("flags")
        self.is_viable = kwargs.get("isViable")
        self.on_base_power_priority = kwargs.get("onBasePowerPriority")
        self.id = kwargs.get("id")  # pylint: disable=C0103
        self.num = kwargs.get("num")
        self._self = kwargs.get("_self")
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
        self.boosts = kwargs.get("boosts")
        self.target = kwargs.get("target")
        self.priority = kwargs.get("priority")

    def calculate_damage(self, attacker, defender, testing=False):
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
        if self.category == "Status":
            return damage, critical_hit

        # Calculate actual damage
        damage = floor(2*attacker["level"]/5 + 2)
        damage = damage * self.base_power
        if self.category == "Physical":
            damage = floor(damage * attacker.effective_stat("atk")) / \
                defender.effective_stat("def")
        elif self.category == "Special":
            damage = floor(damage * attacker.effective_stat("spa")) / \
                defender.effective_stat("spd")
        damage = floor(damage/50) + 2

        # Damage Modifier
        modifier = self.calculate_modifier(attacker, defender)

        # Only apply crits & random range when not testing
        if not testing:
            # Critical Hit
            if random() < 0.0625:
                critical_hit = True
                modifier = modifier * 1.5

            # Random Damage range
            modifier = modifier * uniform(0.85, 1.00)

        damage = floor(damage*modifier)

        return (damage, critical_hit)

    def calculate_modifier(self, attacker, defender):
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
        if self.type in attacker["types"]:
            modifier = modifier * 1.5

        # Weakness modifier
        for def_type in defender["types"]:
            if self.type in WEAKNESS_CHART[def_type]:
                modifier = modifier * WEAKNESS_CHART[def_type][self.type]

        return modifier

    def apply_secondary_effect(self, attacker, defender):
        """
        Apply secondary effects of this move.

        Args:
            attacker (Pokemon): The pokemon using the attack.
            defender (Pokemon): The pokemon that is recieving the attack.

        """

    def apply_boosts(self, attacker, defender):
        """
        Apply primary boosting effect of move.

        Args:
            attacker (Pokemon): The pokemon using the attack.
            defender (Pokemon): The pokemon that is recieving the attack.

        """

    def apply_volatile_status(self, attacker, defender):
        """
        Apply volatile status of this move.

        Args:
            attacker (Pokemon): The pokemon using the attack.
            defender (Pokemon): The pokemon that is recieving the attack.

        """

    def apply_healing(self, attacker, defender):
        """
        Healing effects for a move.

        Args:
            attacker (Pokemon): The pokemon using the attack.
            defender (Pokemon): The pokemon that is recieving the attack.

        """

    def check_hit(self):
        """Check if the move hits."""
        move_acc = self.accuracy
        if isinstance(move_acc, bool):
            return move_acc

        return 100*random() < move_acc

    def to_json(self):
        """Return JSON serializable version of self."""
        return self.__dict__

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


class OHKOMove(BaseMove):
    """Class for OHKO moves."""

    def calculate_damage(self, attacker, defender, testing=False):
        """Damage for an OHKO move is the target's HP."""
        return defender.current_hp, False


class SecondaryEffectMove(BaseMove):
    """Class for moves with secondary effects."""

    def apply_secondary_effect(self, attacker, defender):
        """Apply secondary effects for this move."""
        # Check for type immunity (will be told by damage modifier)
        if self.calculate_modifier(attacker, defender) == 0:
            return

        secondary_effects = self.secondary
        if uniform(0, 100) < secondary_effects["chance"]:
            # Apply secondary effect to player
            if "self" in secondary_effects:
                secondary_effect_logic(attacker, secondary_effects["self"])

            # Apply secondary effects to the opponent
            secondary_effect_logic(defender, secondary_effects)


class BoostingMove(BaseMove):
    """Class for Boosting Moves."""

    def apply_boosts(self, attacker, defender):
        """Apply boosting (primary) effect of move."""
        if self.target == "self":
            for stat in self.boosts:
                attacker.set_boost(stat, self.boosts[stat])
        else:
            for stat in self.boosts:
                defender.set_boost(stat, self.boosts[stat])


class VolatileStatusMove(BaseMove):
    """Class for moves with VOlatile Status."""

    def apply_volatile_status(self, attacker, defender):
        """Apply volatile status of this move."""
        # Handle Substitute
        if self.volatile_status == "Substitute":
            substitute_hp = floor(attacker.max_hp / 4.0)
            if attacker.current_hp > substitute_hp:
                attacker.set_volatile_status("substitute", substitute_hp)
                attacker.current_hp -= substitute_hp
        # Handle applying volatile statuses to the attacker
        elif self._self and "volatileStatus" in self._self:
            if self._self["volatileStatus"] not in attacker.volatile_status:
                if self._self["volatileStatus"] == "lockedmove":
                    attacker.set_volatile_status("lockedmove", {
                        "counter": 0,
                        "move": self
                    })
                else:
                    attacker.set_volatile_status(self._self["volatileStatus"])
        elif self.target == "self" and self.volatile_status:
            attacker.set_volatile_status(self.volatile_status)
        # Handle applying volatile status to defending pokemon
        elif self.volatile_status and self.volatile_status not in defender.volatile_status:
            # Handle Torment (default to None)
            if self.volatile_status == "torment":
                defender.set_volatile_status(self.volatile_status, None)
            # Moves with effect
            if self.effect:
                vol_stat = {}
                vol_stat["effect"] = self.effect
                vol_stat["counter"] = 0
                defender.set_volatile_status(self.volatile_status, vol_stat)
            # All other cases
            else:
                defender.set_volatile_status(self.volatile_status)


class HealingMove(BaseMove):
    """Class for Healing Moves."""

    def apply_healing(self, attacker, defender):
        """Healing effects for a move."""
        if "heal" in self and self["heal"]:
            heal_factor = self["heal"][0]/self["heal"][1]
        else:
            heal_factor = 0.5

        heal_amount = floor(heal_factor * attacker.max_hp)

        # No overheal
        if self.get("target") == "any":
            defender.current_hp = min(defender.max_hp, defender.current_hp + heal_amount)
        else:
            attacker.current_hp = min(attacker.max_hp, attacker.current_hp + heal_amount)


def secondary_effect_logic(target_poke, secondary_effects):
    """Apply secondary effect logic to a player's pokemon."""
    # Apply boosts
    if "boosts" in secondary_effects:
        for stat in secondary_effects["boosts"]:
            target_poke.set_boost(stat, secondary_effects["boosts"][stat])

    # Apply status effects
    if "status" in secondary_effects and target_poke.status is None:
        # Check for type immunity
        type_immunity = False
        for type_ in target_poke.types:
            if type_ in STATUS_IMMUNITIES[secondary_effects["status"]]:
                type_immunity = True

        if not type_immunity:
            target_poke.status = secondary_effects["status"]

    # Apply secondary volatile status
    secondary_vs = secondary_effects.get("volatileStatus", None)
    if secondary_vs is not None and secondary_vs not in target_poke.volatile_status:
        target_poke.volatile_status[secondary_vs] = 0


def generate_move(move_config):
    """
    Dynamically generate a Move's class given its config.

    Args:
        move_config (dict): JSON config for move from moves.json

    """
    output = None
    classes = [BaseMove]

    if move_config.get("volatileStatus") or move_config.get("_self", {}).get("volatileStatus"):
        classes.append(VolatileStatusMove)

    if move_config.get("ohko"):
        classes.append(OHKOMove)

    if move_config.get("boosts"):
        classes.append(BoostingMove)

    if move_config.get("secondary"):
        classes.append(SecondaryEffectMove)

    if move_config.get("flags", {}).get("heal"):
        classes.append(HealingMove)

    # Remove BaseMove if another class defined
    if len(classes) > 1:
        classes.remove(BaseMove)

    class NewClass(*classes):
        """Dynamically define a class inheriting from chosen classes above."""

    output = NewClass(**move_config)

    return output
