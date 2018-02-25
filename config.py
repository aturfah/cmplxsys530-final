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
with open("data/moves/sample_dex.json") as dex_file:
    POKEMON_DATA = json.load(dex_file)
