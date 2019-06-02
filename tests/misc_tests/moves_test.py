"""Test script for Moves."""

from math import floor

from pokemon_helpers.pokemon import Pokemon

from pokemon_helpers.moves import (BaseMove,
                                   OHKOMove,
                                   SecondaryEffectMove,
                                   BoostingMove,
                                   VolatileStatusMove,
                                   HealingMove,
                                   generate_move)
from config import (MOVE_DATA, PAR_STATUS, PSN_STATUS)


def test_base_init():
    """Test the initialization of a BaseMove class."""
    # Default initialization, everything is None
    bm1 = BaseMove(**{})
    assert bm1.num is None

    bm2 = BaseMove(**{"num": -1, "doot": "doot"})
    assert bm2.num == -1


def test_brakcet_op():
    """Test that [] works on BaseMove."""
    bm1 = BaseMove(**{})
    assert bm1.name == bm1["name"] == bm1.get("name")
    assert "name" in bm1


def test_calculate_damage():
    """Test that damage is calculated properly."""
    tackle = BaseMove(**MOVE_DATA["tackle"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

    damage, _ = tackle.calculate_damage(exploud, floatzel, True)
    assert damage == 78


def test_calculate_damage_laserfocus():
    """Test that Laser Focus guarantees a crit."""
    tackle = BaseMove(**MOVE_DATA["tackle"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

    # TODO: Break out testing logic to be no_crits and no_variance
    num_runs = 500
    non_laserfocus_dmg = 0
    laserfocus_dmg = 0
    for _ in range(num_runs):
        damage, _ = tackle.calculate_damage(exploud, floatzel, True)
        non_laserfocus_dmg += damage

    exploud.volatile_status["laserfocus"] = 0
    for _ in range(num_runs):
        damage, _ = tackle.calculate_damage(exploud, floatzel)
        laserfocus_dmg += damage

    # Proxy for not actually having a way to enforce no range
    assert non_laserfocus_dmg * 1.3 < laserfocus_dmg


def test_calculate_modifier():
    """Test that modifier is calculated properly."""
    tackle = BaseMove(**MOVE_DATA["tackle"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])
    gengar = Pokemon(name="gengar", moves=["tackle"])
    regirock = Pokemon(name="regirock", moves=["selfdestruct"])

    assert tackle.calculate_modifier(exploud, gengar) == 0  # No Effect
    assert tackle.calculate_modifier(exploud, floatzel) == 1.5  # STAB
    assert tackle.calculate_modifier(floatzel, regirock) == 0.5  # Not Very Effective
    assert tackle.calculate_modifier(exploud, regirock) == 0.75  # Multiply together


def test_check_hit():
    """Test that move accuracy is calculated properly."""
    hydro_pump = BaseMove(**MOVE_DATA["hydropump"])
    aerial_ace = BaseMove(**MOVE_DATA["aerialace"])
    sheer_cold = BaseMove(**MOVE_DATA["sheercold"])
    fire_punch = BaseMove(**MOVE_DATA["firepunch"])
    num_trials = 500

    num_hp_hits = 0
    num_sc_hits = 0
    num_aa_hits = 0
    num_fp_hits = 0
    for _ in range(num_trials):
        if hydro_pump.check_hit():
            num_hp_hits += 1
        if sheer_cold.check_hit():
            num_sc_hits += 1
        if aerial_ace.check_hit():
            num_aa_hits += 1
        if fire_punch.check_hit():
            num_fp_hits += 1

    assert num_hp_hits < num_trials  # Hydro Pump ssometimes miss (80% Accuracy)
    assert num_aa_hits == num_trials  # Aerial Ace should never miss (T/F case)
    assert num_sc_hits < num_hp_hits  # Sheer Cold should rarely hit (30% Accuracy)
    assert num_fp_hits == num_trials    # Fire Punch also shouldn't miss


def test_ohko_move():
    """Test that OHKO moves do target's current HP worth of damage."""
    sheer_cold = OHKOMove(**MOVE_DATA["sheercold"])
    exploud = Pokemon(name="exploud", moves=["return"])
    floatzel = Pokemon(name="floatzel", moves=["shadowball"])

    assert sheer_cold.calculate_damage(exploud, floatzel)[0] == floatzel.current_hp


def test_secondary_effects():
    """Main testing driver for secondary effects."""
    test_opp_2ndary_stat_change()
    test_player_2ndary_stat_changes()
    test_2ndary_status()
    test_2ndary_vs()


def test_opp_2ndary_stat_change():
    """Test secondary effects that involve opponent's stat changes."""
    spinda = Pokemon(name="spinda", moves=["lowsweep"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    low_sweep = SecondaryEffectMove(**MOVE_DATA["lowsweep"])

    # Assert scyther is at -1 Speed
    low_sweep.apply_secondary_effect(spinda, scyther_target)
    assert scyther_target.boosts["spe"] == -1

    # Assert that stat doesn't get lower than -6
    for _ in range(10):
        low_sweep.apply_secondary_effect(spinda, scyther_target)
    assert scyther_target.boosts["spe"] == -6

    # Test that if on damage happens, stat drops don't
    # Ex: Fighting move to Ghost-type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])

    low_sweep.apply_secondary_effect(spinda, gengar_target)
    assert gengar_target.boosts["spe"] == 0


def test_player_2ndary_stat_changes():
    """Test for secondary stat changes to self."""
    spinda = Pokemon(name="spinda", moves=["poweruppunch"])
    scyther_target = Pokemon(name="scyther", moves=["synthesis"])

    powerup_punch = SecondaryEffectMove(**MOVE_DATA["poweruppunch"])

    # Assert that spinda's attack is +1
    powerup_punch.apply_secondary_effect(spinda, scyther_target)
    assert spinda.boosts["atk"] == 1

    # Assert that stat doesn't get higher than +6
    for _ in range(10):
        powerup_punch.apply_secondary_effect(spinda, scyther_target)
    assert spinda.boosts["atk"] == 6

    # Test that if on damage happens, stat drops don't
    # Ex: Fighting move to Ghost-type
    gengar_target = Pokemon(name="gengar", moves=["synthesis"])
    spinda.boosts["atk"] = 0

    powerup_punch.apply_secondary_effect(spinda, gengar_target)
    assert spinda.boosts["atk"] == 0


def test_2ndary_status():
    """Status effects as secondary effect."""
    spinda = Pokemon(name="spinda", moves=["nuzzle", "inferno"])
    charizard_target = Pokemon(name="charizard", moves=["synthesis", "recover"])

    nuzzle = SecondaryEffectMove(**MOVE_DATA["nuzzle"])
    inferno = SecondaryEffectMove(**MOVE_DATA["inferno"])

    # Assert that Muk gets paralyzed
    nuzzle.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status == PAR_STATUS

    # Assert that if there's another status effect, it
    # cannot be overwritten
    charizard_target.status = PSN_STATUS
    nuzzle.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status == PSN_STATUS

    # Assert that the type immunities are respected
    charizard_target.status = None

    inferno.apply_secondary_effect(spinda, charizard_target)
    assert charizard_target.status is None

    # Assert that if no damage, no status effect
    trapinch_target = Pokemon(name="trapinch", moves=["synthesis"])

    nuzzle.apply_secondary_effect(spinda, trapinch_target)
    assert trapinch_target.status is None


def test_boosting_moves():
    """Test boosting moves work properly."""
    swords_dance = BoostingMove(**MOVE_DATA["swordsdance"])
    leer = BoostingMove(**MOVE_DATA["leer"])

    spinda = Pokemon(name="spinda", moves=["nuzzle", "inferno"])
    charizard_target = Pokemon(name="charizard", moves=["synthesis", "recover"])

    # Increase own stats
    swords_dance.apply_boosts(spinda, charizard_target)
    assert spinda.boosts["atk"] == 2

    # Cannot increase own stats beyond +6
    for _ in range(10):
        swords_dance.apply_boosts(spinda, charizard_target)
    assert spinda.boosts["atk"] == 6

    # Decrease opponents' stats
    leer.apply_boosts(spinda, charizard_target)
    assert charizard_target.boosts["def"] == -1

    # Cannot decrease stats beyond -6
    for _ in range(10):
        leer.apply_boosts(spinda, charizard_target)
    assert charizard_target.boosts["def"] == -6


def test_volatile_status():
    """Test to ensure volatile statuses work."""
    test_primary_vs()
    test_substitute_vs()
    test_lockedmove_vs()
    test_primary_vs_edges()


def test_primary_vs():
    """Test that primary volatileStatus is set properly."""
    chimchar_confuse = Pokemon(name="chimchar", moves=["confuseray"])
    chimchar_uproar = Pokemon(name="spinda", moves=["uproar"], nature="timid")

    confuse_ray = VolatileStatusMove(**MOVE_DATA["confuseray"])
    uproar = VolatileStatusMove(**MOVE_DATA["uproar"])

    confuse_ray.apply_volatile_status(chimchar_confuse, chimchar_uproar)
    uproar.apply_volatile_status(chimchar_uproar, chimchar_confuse)

    # Check volatile status applied
    assert chimchar_uproar.volatile_status
    assert chimchar_uproar.volatile_status["confusion"] == 0
    assert chimchar_uproar.volatile_status["uproar"] == 0


def test_2ndary_vs():
    """Test volatile statusses that occur as secondary effects."""
    num_runs = 500
    num_flinch = 0

    torkoal_defend = Pokemon(name="torkoal", moves=["synthesis"])
    chimchar_attak = Pokemon(name="chimchar", moves=["ironhead"])

    iron_head = SecondaryEffectMove(**MOVE_DATA["ironhead"])

    for _ in range(num_runs):
        torkoal_defend.volatile_status = {}
        iron_head.apply_secondary_effect(chimchar_attak, torkoal_defend)
        if "flinch" in torkoal_defend.volatile_status:
            num_flinch += 1

    assert num_flinch > 0
    assert num_flinch < num_runs


def test_primary_vs_edges():
    """Test volatile statuse edge cases."""
    attract = VolatileStatusMove(**MOVE_DATA["attract"])
    automotize = VolatileStatusMove(**MOVE_DATA["autotomize"])
    bane_bunk = VolatileStatusMove(**MOVE_DATA["banefulbunker"])

    defend = Pokemon(name="torkoal", moves=["synthesis"])
    attack = Pokemon(name="chimchar", moves=["ironhead"])

    attract.apply_volatile_status(attack, defend)
    assert attack.volatile_status == {}
    assert "attract" in defend.volatile_status

    attack.volatile_status = {}
    defend.volatile_status = {}
    automotize.apply_volatile_status(attack, defend)
    assert "autotomize" in attack.volatile_status
    assert defend.volatile_status == {}

    attack.volatile_status = {}
    defend.volatile_status = {}
    bane_bunk.apply_volatile_status(attack, defend)
    assert "banefulbunker" in attack.volatile_status
    assert defend.volatile_status == {}


def test_substitute_vs():
    """Make sure substitute is handled properly."""
    exploud = Pokemon(name="exploud", moves=["substitute"])
    spinda_target = Pokemon(name="spinda", moves=["tackle"])

    substitute = VolatileStatusMove(**MOVE_DATA["substitute"])

    sub_hp = floor(exploud.max_hp / 4.0)
    substitute.apply_volatile_status(exploud, spinda_target)

    # Make sure volatile status applied
    assert exploud.volatile_status
    assert "substitute" in exploud.volatile_status

    # Make sure substitute calculated properly.
    assert exploud.volatile_status["substitute"] == sub_hp
    assert exploud.max_hp == sub_hp + exploud.current_hp


def test_lockedmove_vs():
    """Make sure lockedmove is handled properly."""
    dragonite = Pokemon(name="dragonite", moves=["outrage"])
    aggron_target = Pokemon(name="aggron", moves=["recover"])

    outrage = VolatileStatusMove(**MOVE_DATA["outrage"])
    outrage.apply_volatile_status(dragonite, aggron_target)

    assert dragonite.volatile_status
    assert "lockedmove" in dragonite.volatile_status
    assert dragonite.volatile_status["lockedmove"]["move"] == outrage
    assert dragonite.volatile_status["lockedmove"]["counter"] == 0


def test_generate_move():
    """Test that the generate_move function properly generates a move."""
    # Test regular move is only a BaseMove
    tackle_move = generate_move(MOVE_DATA["tackle"])
    assert tackle_move.__class__.__bases__ == (BaseMove, )

    # Test a move that has Volatile Status is only SecondaryEffectMove
    uproar_move = generate_move(MOVE_DATA["uproar"])
    confuseray_move = generate_move(MOVE_DATA["confuseray"])

    assert uproar_move.__class__.__bases__ == (VolatileStatusMove, )
    assert confuseray_move.__class__.__bases__ == (VolatileStatusMove, )

    # Test Boosting Moves are only BoostingMove
    sd_move = generate_move(MOVE_DATA["swordsdance"])
    assert sd_move.__class__.__bases__ == (BoostingMove, )

    # Test OHKO moves
    sheercold_move = generate_move(MOVE_DATA["sheercold"])
    assert sheercold_move.__class__.__bases__ == (OHKOMove, )

    # Test Healing moves
    synthesis_move = generate_move(MOVE_DATA["synthesis"])
    assert synthesis_move.__class__.__bases__ == (HealingMove, )

    # Test Secondary Effect moves
    lowsweep_move = generate_move(MOVE_DATA["lowsweep"])
    pup_move = generate_move(MOVE_DATA["poweruppunch"])
    nuzzle_move = generate_move(MOVE_DATA["nuzzle"])
    assert lowsweep_move.__class__.__bases__ == (SecondaryEffectMove, )
    assert pup_move.__class__.__bases__ == (SecondaryEffectMove, )
    assert nuzzle_move.__class__.__bases__ == (SecondaryEffectMove, )


def test_healing():
    """Make sure healing is applied."""
    ivysaur = Pokemon(name="ivysaur", moves=["synthesis"])
    floatzel = Pokemon(name="floatzel", moves=["watergun"])

    ivysaur.current_hp = 1
    floatzel.current_hp = 1

    synthesis = HealingMove(**MOVE_DATA["synthesis"])
    heal_pulse = HealingMove(**MOVE_DATA["healpulse"])

    # Ivysaur uses Synthesis
    synthesis.apply_healing(ivysaur, floatzel)
    assert ivysaur.current_hp == 1 + int(ivysaur.max_hp / 2)
    assert floatzel.current_hp == 1

    # Ivysaur uses Heal Pulse on Floatzel
    heal_pulse.apply_healing(ivysaur, floatzel)
    assert ivysaur.current_hp == 1 + int(ivysaur.max_hp / 2)
    assert floatzel.current_hp == 1 + int(ivysaur.max_hp / 2)

    # No Overheal
    synthesis.apply_healing(ivysaur, floatzel)
    assert ivysaur.current_hp == ivysaur.max_hp


test_base_init()
test_brakcet_op()
test_calculate_damage()
test_calculate_damage_laserfocus()
test_calculate_modifier()
test_check_hit()
test_ohko_move()
test_secondary_effects()
test_boosting_moves()
test_volatile_status()
test_generate_move()
test_healing()
