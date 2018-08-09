"""Class to read teams from a directory."""

from os import listdir


class TeamReader:
    """
    Team Reader Class.

    Attributes:
        team_files = List of filenames for the teams
    """

    def __init__(self, teams_directory="data/teams", prefix=None, suffix=None):
        """Initialization method."""
        team_file_list = listdir(teams_directory)

        if prefix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.startswith(prefix)]

        if suffix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.endswith(suffix)]

        print(team_file_list)
        self.team_files = team_file_list
