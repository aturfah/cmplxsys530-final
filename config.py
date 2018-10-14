"""Config file with directory info."""
import os
from os import listdir
from os.path import isfile, join

import json

# Log file directory
LOG_DIR = "logs/"
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

# Store move data
MOVE_DATA = None
with open("data/moves/moves.json") as move_file:
    MOVE_DATA = json.load(move_file)

# Store pokemon (stats) data
POKEMON_DATA = None
with open("data/pokemon/dex.json") as dex_file:
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

USAGE_STATS = {}
for filename in [name for name in listdir("data/usage/") if isfile(join("data/usage", name))]:
    with open(join("data/usage/", filename)) as usage_file:
        tier = None
        if "pu" in filename:
            tier = "pu"
        if "1630" not in filename:
            continue
        USAGE_STATS["pu"] = json.load(usage_file)["data"]
TEMP_DICT = {}
for poke_name in USAGE_STATS["pu"]:
    mod_name = poke_name.lower()
    TEMP_DICT[mod_name] = USAGE_STATS["pu"][poke_name]
USAGE_STATS["pu"] = TEMP_DICT
del TEMP_DICT

# Status strings
PAR_STATUS = "par"
FRZ_STATUS = "frz"
SLP_STATUS = "slp"
BRN_STATUS = "brn"
PSN_STATUS = "psn"
TOX_STATUS = "tox"
