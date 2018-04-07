"""Main Flask App for Agent Interface"""

import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

# Engine Imports
from battle_engine.rockpaperscissors import RPSEngine
from battle_engine.pokemon_engine import PokemonEngine

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
    "pkmn": PokemonEngine
}

OPPONENT = None
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
    global ENGINE, OPPONENT

    req_data = json.loads(request.data)

    game_choice = req_data["game_choice"]
    opp_choice = req_data["opp_choice"]

    ENGINE = ENGINE_DICT[game_choice]()

    if game_choice == "pkmn":
        opp_team = TEAM_DICT[req_data.get("team_choice", None)]
        OPPONENT = OPPONENT_DICT[opp_choice](team=opp_team)

    return jsonify({})
