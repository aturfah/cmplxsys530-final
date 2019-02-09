"""Testing script for the pkmn_player_gamestate class."""

from battle_engine.pokemon_engine import anonymize_gamestate_helper

from config import MOVE_DATA

from pokemon_helpers.pokemon import Pokemon
from pokemon_helpers.pkmn_player_gamestate import PokemonPlayerGameState
from pokemon_helpers.moves import generate_move

def basic_test():
    """Test initializing and accessing of attributes."""
    ppgs = PokemonPlayerGameState()

    # Attribute lookup
    assert not ppgs.test_attr

    # Setting values in that dictionary
    ppgs.test_attr["test"] = 7
    assert ppgs.test_attr
    assert ppgs.test_attr["test"] == 7


def test_reset_gamestates():
    """Test that resetting a gamestate works."""
    ppgs = PokemonPlayerGameState()

    # Set the values in the gamestate
    ppgs.gamestate["doot"] = 7
    ppgs.opp_gamestate["data"]["pew"] = 71

    assert ppgs.gamestate
    assert ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]
    assert not ppgs.opp_gamestate["investment"]

    # Now reset them
    ppgs.reset_gamestates()
    assert not ppgs.gamestate
    assert not ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]
    assert not ppgs.opp_gamestate["investment"]


def test_init_opp_gamestate():
    """Test that initializing an opponent's gamestate works."""
    ppgs = PokemonPlayerGameState()

    # Initialize opponent's gamestate
    spinda = Pokemon(name="spinda", moves=["tackle"])
    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda
    ppgs.init_opp_gamestate(gamestate["team"], gamestate["active"])

    # Assert that only investment was calculated
    assert ppgs.opp_gamestate["investment"]
    assert not ppgs.opp_gamestate["data"]
    assert not ppgs.opp_gamestate["moves"]

    # Assert that values were filled in properly
    assert ppgs.opp_gamestate["investment"]["spinda"]["hp"]
    assert [int(x) for x in ppgs.opp_gamestate["investment"]["spinda"]["spe"]] == [140, 240]


def test_opp_gamestate():
    """Test that opponent's gamestate is updated properly."""
    spinda = Pokemon(name="spinda", moves=["tackle"])

    ppgs1 = PokemonPlayerGameState()
    ppgs2 = PokemonPlayerGameState()

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = spinda

    opp_gamestate = anonymize_gamestate_helper(gamestate)

    # Update the gamestate
    ppgs1.update_gamestate(gamestate, opp_gamestate)
    ppgs2.update_gamestate(gamestate, opp_gamestate)

    # Gamestate updating happens properly.
    assert ppgs1.opp_gamestate["data"]
    assert not ppgs1.opp_gamestate["data"]["team"]
    assert ppgs1.opp_gamestate["data"]["active"]["name"] == "spinda"

    turn_info = {}
    turn_info["type"] = "ATTACK"
    turn_info["attacker"] = "player2"
    turn_info["move"] = spinda.moves[0]
    turn_info["pct_damage"] = 28
    turn_info["def_poke"] = "spinda"
    turn_info["atk_poke"] = "spinda"
    turn_info = [turn_info]

    # Give new info
    ppgs1.new_info(turn_info, "player1")
    # New info is stored properly
    assert len(ppgs1.opp_gamestate["moves"]["spinda"]) == 1


def test_infer_investment():
    """Make sure investment is properly inferred."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    ppgs1 = PokemonPlayerGameState()
    ppgs2 = PokemonPlayerGameState()

    # Set the gamestate
    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp
    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = spinda
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    ppgs1.update_gamestate(gamestate, opp_gamestate)
    ppgs2.update_gamestate(opp_gamestate_dict,
                           anonymize_gamestate_helper(gamestate))

    # Set the new info
    new_info = {}
    new_info["type"] = "ATTACK"
    new_info["move"] = generate_move(MOVE_DATA["tackle"])
    new_info["attacker"] = "player1"
    new_info["defender"] = "player2"
    new_info["pct_damage"] = 27
    new_info["damage"] = 46
    new_info["atk_poke"] = "spinda"
    new_info["def_poke"] = "magikarp"
    new_info = [new_info]

    test_infer_defending(ppgs2, new_info)
    test_infer_attacking(ppgs1, new_info)
    test_infer_speed_investment()

    # Test with misses
    ppgs1 = PokemonPlayerGameState()
    ppgs1.update_gamestate(gamestate, opp_gamestate)
    test_infer_miss(ppgs1)


def test_infer_defending(ppgs2, new_info):
    """Make sure opponent attack investment is properly inferred."""
    ppgs2.new_info(new_info, "player2")
    assert ppgs2.opp_gamestate["investment"]
    assert ppgs2.opp_gamestate["investment"]["spinda"]
    assert ppgs2.opp_gamestate["investment"]["spinda"]["atk"]
    assert "def" not in ppgs2.opp_gamestate["investment"]["spinda"]
    assert len(ppgs2.opp_gamestate["investment"]["spinda"]["atk"]) == 2
    assert not ppgs2.opp_gamestate["investment"]["spinda"]["atk"][0]["max_evs"]
    assert not ppgs2.opp_gamestate["investment"]["spinda"]["atk"][0]["positive_nature"]
    assert not ppgs2.opp_gamestate["investment"]["spinda"]["atk"][1]["max_evs"]
    assert ppgs2.opp_gamestate["investment"]["spinda"]["atk"][1]["positive_nature"]

    new_info[0]["pct_damage"] = 25
    ppgs2.new_info(new_info, "player2")
    assert len(ppgs2.opp_gamestate["investment"]["spinda"]["atk"]) == 1
    assert not ppgs2.opp_gamestate["investment"]["spinda"]["atk"][0]["max_evs"]
    assert not ppgs2.opp_gamestate["investment"]["spinda"]["atk"][0]["positive_nature"]


def test_infer_attacking(ppgs1, new_info):
    """Make sure opponent defense investment is properly determined."""
    ppgs1.new_info(new_info, "player1")

    assert ppgs1.opp_gamestate["investment"]
    assert ppgs1.opp_gamestate["investment"]["magikarp"]
    assert ppgs1.opp_gamestate["investment"]["magikarp"]["def"]
    assert "atk" not in ppgs1.opp_gamestate["investment"]["magikarp"]
    assert len(ppgs1.opp_gamestate["investment"]["magikarp"]["def"]) == 2
    assert len(ppgs1.opp_gamestate["investment"]["magikarp"]["hp"]) == 2
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["def"][0]["max_evs"]
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["def"][0]["positive_nature"]
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["def"][1]["max_evs"]
    assert ppgs1.opp_gamestate["investment"]["magikarp"]["def"][1]["positive_nature"]

    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["hp"][0]["max_evs"]
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["hp"][1]["max_evs"]

    new_info[0]["pct_damage"] = 29
    ppgs1.new_info(new_info, "player1")

    assert len(ppgs1.opp_gamestate["investment"]["magikarp"]["def"]) == 1
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["def"][0]["max_evs"]
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["def"][0]["positive_nature"]
    assert not ppgs1.opp_gamestate["investment"]["magikarp"]["hp"][0]["max_evs"]


def test_infer_speed_investment():
    """Test how we infer speed."""
    magikarp = Pokemon(name="magikarp", moves=["tackle"])
    spinda = Pokemon(name="spinda", moves=["tackle"])

    ppgs1 = PokemonPlayerGameState()
    ppgs2 = PokemonPlayerGameState()

    gamestate = {}
    gamestate["team"] = []
    gamestate["active"] = magikarp
    opp_gamestate_dict = {}
    opp_gamestate_dict["team"] = []
    opp_gamestate_dict["active"] = spinda
    opp_gamestate = anonymize_gamestate_helper(opp_gamestate_dict)
    ppgs1.update_gamestate(gamestate, opp_gamestate)
    ppgs2.update_gamestate(opp_gamestate_dict,
                           anonymize_gamestate_helper(gamestate))

    new_info = {}
    new_info["type"] = "ATTACK"
    new_info["move"] = generate_move(MOVE_DATA["tackle"])
    new_info["attacker"] = "player2"
    new_info["defender"] = "player1"
    new_info["pct_damage"] = 27
    new_info["damage"] = 46
    new_info["atk_poke"] = "spinda"
    new_info["def_poke"] = "magikarp"
    new_info = [new_info] * 2

    test_infer_speed_faster(ppgs2, new_info)
    test_infer_speed_slower(ppgs1, new_info)


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


def test_infer_miss(player_gs):
    """Infer on a miss."""
    new_info = [{'type': 'ATTACK',
                 'move': generate_move(MOVE_DATA["hydropump"]),
                 'critical_hit': False,
                 'damage': 0,
                 'pct_damage': 0.0,
                 'attacker': "player2",
                 'defender': "player1",
                 'atk_poke': 'spinda',
                 'def_poke': 'magikarp', 'move_hits': False}]

    original_investment = player_gs.opp_gamestate["investment"]
    player_gs.new_info(new_info, "player1")

    # Got new move info
    assert "spinda" in player_gs.opp_gamestate["moves"]
    assert player_gs.opp_gamestate["moves"]["spinda"]

    # Did not do any inference on investment
    assert player_gs.opp_gamestate["investment"] == original_investment


basic_test()
test_reset_gamestates()
test_init_opp_gamestate()
test_infer_investment()
