"""Class for a pokemon used by a PokemonAgent."""

from config import MOVE_DATA
from config import POKEMON_DATA


class Pokemon:
    """The pokemon class."""

    def __init__(self, name, moves, level=100):
        """Initialize a pokemon."""
        # Validate pokemon chosen
        if name not in POKEMON_DATA:
            raise AttributeError("Invalid pokemon chosen: {}.".format(name))

        # Validate moves
        if not moves:
            raise AttributeError("Moves must be provided.")
        for move in moves:
            if move not in MOVE_DATA:
                raise AttributeError("Invalid move chosen: {}.".format(move))

        # Validate level
        if level not in range(1, 101):
            raise AttributeError("Level must be between 1 and 100")

