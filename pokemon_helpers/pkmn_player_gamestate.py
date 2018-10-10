"""Class defining an Engine's Game State."""


class PokemonPlayerGameState:
    """Representation of a player's internal game state."""

    def __init__(self):
        """Initialize this player's internal game state."""
        self.test = "DOOT"

    def __getitem__(self, key):
        """
        Define [] lookup on this object.

        :param key: str
            Attribute of this object to get.
        """
        return self.__getattribute__(key)
