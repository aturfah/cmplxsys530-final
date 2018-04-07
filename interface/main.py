"""Main Flask App for Agent Interface"""

import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from battle_engine.rockpaperscissors import RPSEngine
from battle_engine.pokemon_engine import PokemonEngine

INTERFACE = Flask(__name__)

ENGINE = None
ENGINE_DICT = {
    "rps": RPSEngine,
    "pkmn": PokemonEngine
}

OPPONENT = None
OPPONENT_DICT = {
    "random_rps": 1,
    "counter_rps": 2,
    "random_pkmn": 3,
    "basic_planning_pkmn": 4,
    "rock_rps": 5,
    "paper_rps": 6,
    "scissors_rps": 7,
    "uniform_rps": 8
}

# pylint: disable=W0603
# I want to use global here.
# Fight me.


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
    global ENGINE, OPPONENT

    req_data = json.loads(request.data)

    game_choice = req_data["game_choice"]
    opp_choice = req_data["opp_choice"]
    opp_team = req_data.get("team_choice", None)

    ENGINE = ENGINE_DICT[game_choice]()
    OPPONENT = OPPONENT_DICT[opp_choice]

    return jsonify({})
