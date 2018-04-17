"""Unit tests for PokemonAgent class."""

from pokemon_helpers.pokemon import Pokemon
from agent.basic_pokemon_agent import PokemonAgent
from battle_engine.pokemon_engine import anonymize_gamestate_helper

from config import MOVE_DATA


def test_make_move():
    """Test that make_move is outputting valid info."""
    spinda = Pokemon(
        name="spinda",
        moves=["tackle", "watergun", "thundershock", "shadowball"])
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([spinda, magikarp, magikarp, magikarp])

    # Set player's gamestate
    pa1.gamestate = {}
    pa1.gamestate["team"] = [magikarp, magikarp, magikarp]
    pa1.gamestate["active"] = spinda

    move_type, val = pa1.make_move()

    assert move_type in ["SWITCH", "ATTACK"]
    if move_type == "SWITCH":
        # Switch to magikarp
        assert val in range(3)
    else:
        # Picks one of 4 moves
        assert val in range(4)


def test_opp_gamestate():
    """Test that opponent's gamestate is updated properly."""
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([spinda])
    pa2 = PokemonAgent([spinda])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    pa1.update_gamestate(gamestate, opp_gamestate)
    pa2.update_gamestate(gamestate, opp_gamestate)

    # Gamestate updating happens properly.
    assert pa1.opp_gamestate["data"]
    assert not pa1.opp_gamestate["data"]["team"]
    assert pa1.opp_gamestate["data"]["active"]["name"] == "spinda"

    turn_info = {}
    turn_info["type"] = "ATTACK"
    turn_info["attacker"] = "player2"
    turn_info["move"] = spinda.moves[0]
    turn_info["pct_damage"] = 28
    turn_info["def_poke"] = "spinda"
    turn_info["atk_poke"] = "spinda"
    turn_info = [turn_info]

    # Give new info
    pa1.new_info(turn_info, "player1")
    # New info is stored properly
    assert len(pa1.opp_gamestate["moves"]["spinda"]) == 1

    # Assert that reseting the gamestate actually does it
    pa2.reset_gamestates()
    assert not pa2.gamestate
    assert not pa2.opp_gamestate["data"]
    assert not pa2.opp_gamestate["moves"]


def test_switch_faint():
    """Test that switch_faint() picks a valid pokemon."""
    exploud = Pokemon(name="exploud", moves=["tackle"])
    pa1 = PokemonAgent([exploud])

    gamestate = {}
    gamestate["team"] = [exploud, exploud, exploud]
    gamestate["active"] = None

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    pa1.update_gamestate(gamestate, opp_gamestate)
    val = pa1.switch_faint()
    assert val in range(3)


def test_battle_posn_one():
    """Test battle position functions work."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    magikarp_opp = Pokemon(name="magikarp", moves=["tackle"])
    pa1 = PokemonAgent([magikarp])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp

    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = magikarp_opp
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)

    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 1
    assert pa1.calc_opp_position() == 1
    assert pa1.battle_position() == 1

    # We're now in a bad position
    magikarp.current_hp = 1
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() < 0.1
    assert pa1.calc_opp_position() == 1
    assert pa1.battle_position() < 1

    # Now we're in a better position.
    magikarp.current_hp = magikarp.max_hp/2
    magikarp_opp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 0.5
    assert pa1.calc_opp_position() < 0.1
    assert pa1.battle_position() > 1


def test_battle_posn_multiple():
    """Test that battle position functions work with multiple pokemon."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    magikarp_opp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([magikarp, spinda, spinda])

    gamestate = {}
    gamestate["team"] = [spinda, spinda]
    gamestate["active"] = magikarp

    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = [spinda]
    opp_gamestate_dict["active"] = magikarp_opp
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)

    # Everything maximum HP
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 3
    assert pa1.calc_opp_position() == 2
    assert pa1.battle_position() == 1.5

    # Good position, opponent has low HP
    magikarp_opp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() == 3
    assert pa1.calc_opp_position() < 2
    assert pa1.calc_opp_position() > 1
    assert pa1.battle_position() > 1.5
    assert pa1.battle_position() < 3

    # Bad position, we have low HP
    magikarp_opp.current_hp = magikarp_opp.max_hp
    magikarp.current_hp = 1
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    assert pa1.calc_position() < 3
    assert pa1.calc_position() > 2
    assert pa1.calc_opp_position() == 2
    assert pa1.battle_position() < 1.5
    assert pa1.calc_position() > 1


def test_infer_investment():
    """Make sure investment is properly inferred."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([magikarp])
    pa2 = PokemonAgent([spinda])

    # Set the gamestate
    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp
    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = spinda
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    pa2.update_gamestate(opp_gamestate_dict,
                         anonymize_gamestate_helper(gamestate))

    # Set the new info
    new_info = {}
    new_info["type"] = "ATTACK"
    new_info["move"] = MOVE_DATA["tackle"]
    new_info["attacker"] = "player1"
    new_info["defender"] = "player2"
    new_info["pct_damage"] = 27
    new_info["damage"] = 46
    new_info["atk_poke"] = "spinda"
    new_info["def_poke"] = "magikarp"
    new_info = [new_info]

    test_infer_defending(pa2, new_info)
    test_infer_attacking(pa1, new_info)
    test_infer_speed_investment()


def test_infer_defending(pa2, new_info):
    """Make sure opponent attack investment is properly inferred."""
    pa2.new_info(new_info, "player2")
    assert pa2.opp_gamestate["investment"]
    assert pa2.opp_gamestate["investment"]["spinda"]
    assert pa2.opp_gamestate["investment"]["spinda"]["atk"]
    assert "def" not in pa2.opp_gamestate["investment"]["spinda"]
    assert len(pa2.opp_gamestate["investment"]["spinda"]["atk"]) == 2
    assert not pa2.opp_gamestate["investment"]["spinda"]["atk"][0]["max_evs"]
    assert not pa2.opp_gamestate["investment"]["spinda"]["atk"][0]["positive_nature"]
    assert not pa2.opp_gamestate["investment"]["spinda"]["atk"][1]["max_evs"]
    assert pa2.opp_gamestate["investment"]["spinda"]["atk"][1]["positive_nature"]

    new_info[0]["pct_damage"] = 25
    pa2.new_info(new_info, "player2")
    assert len(pa2.opp_gamestate["investment"]["spinda"]["atk"]) == 1
    assert not pa2.opp_gamestate["investment"]["spinda"]["atk"][0]["max_evs"]
    assert not pa2.opp_gamestate["investment"]["spinda"]["atk"][0]["positive_nature"]


def test_infer_attacking(pa1, new_info):
    """Make sure opponent defense investment is properly determined."""
    pa1.new_info(new_info, "player1")

    assert pa1.opp_gamestate["investment"]
    assert pa1.opp_gamestate["investment"]["magikarp"]
    assert pa1.opp_gamestate["investment"]["magikarp"]["def"]
    assert "atk" not in pa1.opp_gamestate["investment"]["magikarp"]
    assert len(pa1.opp_gamestate["investment"]["magikarp"]["def"]) == 2
    assert len(pa1.opp_gamestate["investment"]["magikarp"]["hp"]) == 2
    assert not pa1.opp_gamestate["investment"]["magikarp"]["def"][0]["max_evs"]
    assert not pa1.opp_gamestate["investment"]["magikarp"]["def"][0]["positive_nature"]
    assert not pa1.opp_gamestate["investment"]["magikarp"]["def"][1]["max_evs"]
    assert pa1.opp_gamestate["investment"]["magikarp"]["def"][1]["positive_nature"]

    assert not pa1.opp_gamestate["investment"]["magikarp"]["hp"][0]["max_evs"]
    assert not pa1.opp_gamestate["investment"]["magikarp"]["hp"][1]["max_evs"]

    new_info[0]["pct_damage"] = 29
    pa1.new_info(new_info, "player1")

    assert len(pa1.opp_gamestate["investment"]["magikarp"]["def"]) == 1
    assert not pa1.opp_gamestate["investment"]["magikarp"]["def"][0]["max_evs"]
    assert not pa1.opp_gamestate["investment"]["magikarp"]["def"][0]["positive_nature"]
    assert not pa1.opp_gamestate["investment"]["magikarp"]["hp"][0]["max_evs"]


def test_infer_speed_investment():
    """Test how we infer speed."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    pa1 = PokemonAgent([magikarp])
    pa2 = PokemonAgent([spinda])

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp
    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = spinda
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    pa1.update_gamestate(gamestate, opp_gamestate)
    pa2.update_gamestate(opp_gamestate_dict,
                         anonymize_gamestate_helper(gamestate))

    new_info = {}
    new_info["type"] = "ATTACK"
    new_info["move"] = MOVE_DATA["tackle"]
    new_info["attacker"] = "player2"
    new_info["defender"] = "player1"
    new_info["pct_damage"] = 27
    new_info["damage"] = 46
    new_info["atk_poke"] = "spinda"
    new_info["def_poke"] = "magikarp"
    new_info = [new_info] * 2

    test_infer_speed_faster(pa2, new_info)
    test_infer_speed_slower(pa1, new_info)


def test_infer_speed_faster(player, new_info):
    """Test how we infer speed on outspeed."""
    player.new_info(new_info, my_id="player1")

    assert player.opp_gamestate["investment"]
    assert player.opp_gamestate["investment"]["spinda"]
    assert player.opp_gamestate["investment"]["spinda"]["spe"]
    speed_inference = player.opp_gamestate["investment"]["spinda"]["spe"]
    assert speed_inference[1] == 240
    assert speed_inference[0] == player.gamestate["active"].speed


def test_infer_speed_slower(player, new_info):
    """Test how we infer speed when slower."""
    player.new_info(new_info, my_id="player2")

    assert player.opp_gamestate["investment"]
    assert player.opp_gamestate["investment"]["magikarp"]
    assert player.opp_gamestate["investment"]["magikarp"]["spe"]
    speed_inference = player.opp_gamestate["investment"]["magikarp"]["spe"]

    assert speed_inference[1] == player.gamestate["active"].speed
    assert speed_inference[0] == 176


test_make_move()
test_opp_gamestate()
test_switch_faint()
test_battle_posn_one()
test_battle_posn_multiple()
test_infer_investment()
