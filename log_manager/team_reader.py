"""Class to read teams from a directory."""

from os import listdir
from os.path import join

from re import match


class TeamReader:
    """
    Team Reader Class.

    Attributes:
        team_files: List of filenames for the teams
        teams: List of teams

    """

    def __init__(self, teams_directory="data/teams", prefix=None, suffix=None):
        """Initialize a TeamReader."""
        team_file_list = listdir(teams_directory)

        if prefix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.startswith(prefix)]

        if suffix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.endswith(suffix)]

        team_file_list = [join(teams_directory, team_file)
                          for team_file in team_file_list]

        self.team_files = team_file_list
        self.teams = []

    def process_files(self):
        """Read the contents of each file and load them into a list."""
        for filename in self.team_files:
            file_lines = [line.strip() for line in open(filename).readlines()]

            started_pokemon = False
            pokemon_dict = {}
            for line in file_lines:
                if not started_pokemon:
                    started_pokemon = True
                    read_name(line, pokemon_dict)
                elif line.startswith("Ability:"):
                    read_ability(line, pokemon_dict)
                elif line.startswith("EVs:"):
                    read_ev_iv(line.replace("EVs:", ""), pokemon_dict, "ev")
                elif line.startswith("IVs:"):
                    read_ev_iv(line.replace("IVs:", ""), pokemon_dict, "iv")
                elif line.endswith("Nature"):
                    read_nature(line, pokemon_dict)
                elif line.startswith("-"):
                    read_move(line, pokemon_dict)
                else:
                    print(line)


def read_name(input_str, pokemon_dict):
    """Read in a Pokemon's name, and add it to the pokemon_dict."""
    # Try to read an item
    try:
        name_species_gender, item = input_str.strip().rsplit("@", 1)
        item = item.strip()
    except ValueError:
        name_species_gender = input_str.strip()
        item = None

    # Try to parse out Pokemon Gender
    name_species_gender = name_species_gender.strip()
    matches = match(r"^(.+) \(([MF])\)$", name_species_gender)
    if matches:
        name_species, gender = matches.groups()
    else:
        name_species = name_species_gender
        gender = None

    # Try to read nickname/species
    name_species = name_species.strip()
    matches = match(r"^(.+) \((.+)\)$", name_species)
    if matches:
        nickname, species = matches.groups()
    else:
        nickname = name_species
        species = name_species

    # Update the dictionaries
    pokemon_dict["nickname"] = nickname
    pokemon_dict["species"] = species
    pokemon_dict["item"] = item
    pokemon_dict["gender"] = gender
    # print(pokemon_dict)


def read_nature(input_str, pokemon_dict):
    """Read a Pokemon's Nature."""
    nature = input_str.replace("Nature", "").strip()
    pokemon_dict["nature"] = nature
    # print(pokemon_dict)


def read_ability(input_str, pokemon_dict):
    """Read out the Pokemon's ability."""
    ability = input_str.replace("Ability: ", "").strip()
    pokemon_dict["ability"] = ability
    # print(pokemon_dict)


def read_ev_iv(input_str, pokemon_dict, chosen="ev"):
    """Read a Pokemon's EV/IVs."""
    pokemon_dict[chosen] = {}
    value_list = [value_str.strip() for value_str in input_str.split("/")]

    for value_str in value_list:
        value_val, stat = value_str.strip().split()
        pokemon_dict[chosen][stat] = int(value_val)

    # print(pokemon_dict)


def read_move(input_str, pokemon_dict):
    """Read a Pokemon's move."""
    move = input_str.replace("-", "").strip()
    if "moves" not in pokemon_dict:
        pokemon_dict["moves"] = []

    pokemon_dict["moves"].append(move.lower())
    # print(pokemon_dict)


def process_pokemon():
    """Generate a Pokemon from the string in a file."""
    pass
