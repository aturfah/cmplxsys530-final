"""Config file with directory info."""
import os
import json

# Log file directory
LOG_DIR = "logs/"
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

# Store move data
MOVE_DATA = None
with open("data/moves/sample_moves.json") as move_file:
    MOVE_DATA = json.load(move_file)

# Store pokemon (stats) data
POKEMON_DATA = None
with open("data/pokemon/sample_dex.json") as dex_file:
    POKEMON_DATA = json.load(dex_file)

WEAKNESS_CHART = None
with open("data/weakness.json") as weakness_file:
    WEAKNESS_CHART = json.load(weakness_file)

NATURES = {
    "hardy": {
        "increase": None,
        "decrease": None
    },
    "lonely": {
        "increase": "attack",
        "decrease": "defense"
    },
    "brave": {
        "increase": "attack",
        "decrease": "speed"
    },
    "adamant": {
        "increase": "attack",
        "decrease": "sp_attack"
    },
    "naughty": {
        "increase": "attack",
        "decrease": "sp_defense"
    },
    "bold": {
        "increase": "defense",
        "decrease": "attack"
    },
    "docile": {
        "increase": None,
        "decrease": None
    },
    "relaxed": {
        "increase": "defense",
        "decrease": "speed"
    },
    "impish": {
        "increase": "defense",
        "decrease": "sp_attack"
    },
    "lax": {
        "increase": "defense",
        "decrease": "sp_defense"
    },
    "timid": {
        "increase": "speed",
        "decrease": "attack"
    },
    "hasty": {
        "increase": "speed",
        "decrease": "defense"
    },
    "serious": {
        "increase": None,
        "decrease": None
    },
    "jolly": {
        "increase": "speed",
        "decrease": "sp_attack"
    },
    "naive": {
        "increase": "speed",
        "decrease": "sp_defense"
    },
    "modest": {
        "increase": "sp_attack",
        "decrease": "attack"
    },
    "quiet": {
        "increase": "sp_attack",
        "decrease": "speed"
    },
    "mild": {
        "increase": "sp_attack",
        "decrease": "defense"
    },
    "bashful": {
        "increase": None,
        "decrease": None
    },
    "rash": {
        "increase": "sp_attack",
        "decrease": "sp_defense"
    },
    "Calm": {
        "increase": "sp_defense",
        "decrease": "attack"
    },
    "gentle": {
        "increase": "sp_defense",
        "decrease": "defense"
    },
    "sassy": {
        "increase": "sp_defense",
        "decrease": "speed"
    },
    "careful": {
        "increase": "sp_defense",
        "decrease": "sp_attack"
    },
    "quirky": {
        "increase": None,
        "decrease": None
    }
}
