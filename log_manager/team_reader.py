"""Class to read teams from a directory."""

from os import listdir
from os.path import join

class TeamReader:
    """
    Team Reader Class.

    Attributes:
        team_files: List of filenames for the teams
        teams: List of teams
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

        team_file_list = [join(teams_directory, team_file) for team_file in team_file_list]

        self.team_files = team_file_list
        self.teams = []

    def process_files(self):
        """Read the contents of each file and load them into a list."""
        for filename in self.team_files:
            file_lines = [line.strip() for line in open(filename).readlines()]

            started_pokemon = False
            pokemon_dict = {}
            for line in file_lines:
                print(line)
                if not started_pokemon:
                    started_pokemon = True
                    read_name(line, pokemon_dict)
                    print(pokemon_dict)


def read_name(input_str, pokemon_dict):
    """Read in a Pokemon's name, and add it to the pokemon_dict."""
    print("READING NAME: ", input_str)
    name_species, item = input_str.rsplit("@", 1)

    item = item.strip()
    name_species = name_species.strip()

    pokemon_dict["species"] = "Doot"
    pokemon_dict["nickname"] = "Foo"
    pokemon_dict["item"] = item


def process_pokemon():
    """Generate a Pokemon from the string in a file."""
    pass
