"""Class defining an Engine's Game State."""


class PokemonPlayerGameState():
    """Representation of a player's internal game state."""
    def __init__(self):
        """Initialize this player's internal game state."""
        pass

    def __getitem__(self, key):
        """
        Define [] operating on this object.

        :param key: str
            Attribute of this object to get.
        """
        return self.__getattribute__(key)

    def __setattr__(self, key, value):
        """
        Define [] operating on this object.

        :param key: str
            Attribute of this object to get.
        :param value: Object
            Value to set for attribute

        """
        pass
