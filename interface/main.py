"""Main Flask App for Agent Interface"""

import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

# Engine Imports
from battle_engine.rockpaperscissors import RPSEngine
from battle_engine.interactive_pokemon_engine import InteractivePokemonEngine

# Pokemon Imports
from agent.basic_pokemon_agent import PokemonAgent
from agent.basic_planning_pokemon_agent import BasicPlanningPokemonAgent
from pokemon_helpers.pokemon import default_team_floatzel
from pokemon_helpers.pokemon import default_team_ivysaur
from pokemon_helpers.pokemon import default_team_spinda

# pylint: disable=W0603
# I want to use global here.
# Fight me.

INTERFACE = Flask(__name__)

ENGINE = None
ENGINE_DICT = {
    "rps": RPSEngine,
    "pkmn": InteractivePokemonEngine
}

OPPONENT = None
PLAYER = None
OPPONENT_DICT = {
    "random_rps": 1,
    "counter_rps": 2,
    "random_pkmn": PokemonAgent,
    "basic_planning_pkmn": BasicPlanningPokemonAgent,
    "rock_rps": 5,
    "paper_rps": 6,
    "scissors_rps": 7,
    "uniform_rps": 8
}

TEAM_DICT = {
    "floatzel": default_team_floatzel,
    "ivysaur": default_team_ivysaur,
    "spinda": default_team_spinda
}

@INTERFACE.route("/")
def index():
    """Index page."""
    global ENGINE, OPPONENT
    ENGINE = None
    OPPONENT = None
    return render_template('index.html')


@INTERFACE.route("/set_parameters", methods=["POST"])
def set_engine():
    """Set the game for this interface."""
    global ENGINE, OPPONENT, PLAYER
    response = {}

    req_data = json.loads(request.data)

    game_choice = req_data["game_choice"]
    opp_choice = req_data["opp_choice"]

    ENGINE = ENGINE_DICT[game_choice]()

    if game_choice == "pkmn":
        player_team = TEAM_DICT[req_data.get("player_team_choice", None)]()
        opp_team = TEAM_DICT[req_data.get("opp_team_choice", None)]()
        PLAYER = OPPONENT_DICT["basic_planning_pkmn"](team=player_team, tier="pu")
        OPPONENT = OPPONENT_DICT[opp_choice](team=opp_team)
        ENGINE.initialize_battle(PLAYER, OPPONENT)

        # Set the response data
        response["outcome"] = ENGINE.win_condition_met()
        response["player_active"] = ENGINE.game_state["player1"]["active"].__dict__
        response["opp_active"] = ENGINE.game_state["player2"]["active"].__dict__
        response["player_opts"] = process_opts(PLAYER, PLAYER.generate_possibilities()[0])

    return jsonify(response)

@INTERFACE.route("/make_move", methods=["POST"])
def make_move():
    """Process a player's move."""
    global ENGINE, OPPONENT, PLAYER
    response = {}

    req_data = json.loads(request.data)

    player_move = (req_data["move_choice"][0], req_data["move_choice"][1])
    turn_info, outcome = ENGINE.run_turn(player_move, PLAYER, OPPONENT)
    response["turn_info"] = turn_info
    response["outcome"] = outcome

    if not outcome["finished"]:
        response["player_active"] = ENGINE.game_state["player1"]["active"].__dict__
        response["opp_active"] = ENGINE.game_state["player2"]["active"].__dict__
        response["player_opts"] = process_opts(PLAYER, PLAYER.generate_possibilities()[0])

    return jsonify(response)

def process_opts(player, player_opts):
    """Add data to the options to make them human readable."""
    results = []
    for opt in player_opts:
        res = list(opt)
        if opt[0] == "ATTACK":
            # Get move name
            res.append(player.gamestate["active"].moves[opt[1]]["name"])
        else:
            # Get pokemon name
            res.append(player.gamestate["team"][opt[1]].name)
        results.append(res)

    return results
