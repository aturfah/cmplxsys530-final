"""Class to read teams from a directory."""

from os import listdir

class TeamReader:
    """
    Team Reader Class.

    Attributes:
        None.
    """
    def __init__(self, teams_directory="data/teams"):
        """Initialization method."""
        teams_list = listdir(teams_directory)
        print(teams_list)
