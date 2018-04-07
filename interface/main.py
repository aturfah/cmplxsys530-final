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

@INTERFACE.route("/")
def index():
    """Index page."""
    global ENGINE
    engine = None
    return render_template('index.html')

@INTERFACE.route("/set_parameters", methods=["POST"])
def set_engine():
    """Set the game for this interface."""
    global ENGINE

    req_data = json.loads(request.data)

    game_choice = req_data["game_choice"]
    ENGINE = ENGINE_DICT[game_choice]()

    return jsonify({})
