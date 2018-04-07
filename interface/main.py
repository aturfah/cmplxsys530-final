"""Main Flask App for Agent Interface"""

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

@INTERFACE.route("/")
def index():
    """Index page."""
    return render_template('index.html')

@INTERFACE.route("/set_engine", methods=["POST"])
def set_engine():
    """Set the game for this interface."""
    choice = request.form.to_dict(flat=False)
    print(choice)

    return jsonify({})
