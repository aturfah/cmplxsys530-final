"""Class to read teams from a directory."""

from os import listdir
from os.path import join

from re import match

from pokemon_helpers.pokemon import Pokemon


class TeamReader:
    """
    Team Reader Class.

    Attributes:
        team_files: List of filenames for the teams
        teams: List of teams

    """

    def __init__(self, teams_directory="data/teams", prefix=None, suffix=None):
        """
        Initialize a TeamReader.

        Args:
            teams_directory (str): Path to folder to read files from.
            prefix (str): Prefix to look for in filenames.
            suffix (str): Suffix to look for in filenames.

        """
        team_file_list = listdir(teams_directory)

        if prefix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.startswith(prefix)]

        if suffix:
            team_file_list = [
                team_file for team_file in team_file_list if team_file.endswith(suffix)]

        team_file_list = [join(teams_directory, team_file).replace("\\", "/")
                          for team_file in team_file_list]

        self.team_files = team_file_list
        self.teams = []

    def process_files(self):
        """Read the contents of each file and load them into a list."""
        for filename in self.team_files:
            file_lines = [line.strip() for line in open(filename).readlines()]
            file_team = []
            started_pokemon = False
            pokemon_dict = {}
            for line in file_lines:
                if not line:
                    started_pokemon = False
                    if pokemon_dict:
                        file_team.append(process_pokemon(pokemon_dict))
                        pokemon_dict = {}
                elif not started_pokemon:
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
                    raise RuntimeWarning(
                        "Line not recognized and will be ignored: {}".format(line))

            # Account for end of file
            if started_pokemon and pokemon_dict:
                file_team.append(process_pokemon(pokemon_dict))

            self.teams.append(file_team)


def read_name(input_str, pokemon_dict):
    """
    Read in a Pokemon's name, and add it to the pokemon_dict.

    Args:
        input_str (str): Row to read data from.
        pokemon_dict (dict): Dictionary with Pokemon data to update.

    """
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
        species = name_species.replace("-", "")

    # Update the dictionaries
    pokemon_dict["nickname"] = nickname
    pokemon_dict["species"] = species.lower()
    pokemon_dict["item"] = item
    pokemon_dict["gender"] = gender
    # print(pokemon_dict)


def read_nature(input_str, pokemon_dict):
    """
    Read a Pokemon's Nature.

    Args:
        input_str (str): Row to read data from.
        pokemon_dict (dict): Dictionary with Pokemon data to update.

    """
    nature = input_str.replace("Nature", "").strip()
    pokemon_dict["nature"] = nature.lower()
    # print(pokemon_dict)


def read_ability(input_str, pokemon_dict):
    """
    Read out the Pokemon's ability.

    Args:
        input_str (str): Row to read data from.
        pokemon_dict (dict): Dictionary with Pokemon data to update.

    """
    ability = input_str.replace("Ability: ", "").strip()
    pokemon_dict["ability"] = ability
    # print(pokemon_dict)


def read_ev_iv(input_str, pokemon_dict, chosen="ev"):
    """
    Read a Pokemon's EV/IVs.

    Args:
        input_str (str): Row to read data from.
        pokemon_dict (dict): Dictionary with Pokemon data to update.
        chosen (str): One of 'ev' or 'iv', to determine whether to read in EVs
            or IVs

    """
    pokemon_dict[chosen] = {}
    value_list = [value_str.strip() for value_str in input_str.split("/")]

    for value_str in value_list:
        value_val, stat = value_str.strip().split()
        pokemon_dict[chosen][stat.lower()] = int(value_val)

    # print(pokemon_dict)


def read_move(input_str, pokemon_dict):
    """
    Read a Pokemon's move.

    Args:
        input_str (str): Row to read data from.
        pokemon_dict (dict): Dictionary with Pokemon data to update.

    """
    move = input_str.replace("-", "").strip()
    if "moves" not in pokemon_dict:
        pokemon_dict["moves"] = []

    pokemon_dict["moves"].append(move.lower().replace(" ", ""))
    # print(pokemon_dict)


def process_pokemon(pokemon_dict):
    """
    Generate a Pokemon from the string in a file.

    Args:
        pokemon_dict (dict): Dictionary with Pokemon data.

    """
    init_dict = {}
    init_dict["nickname"] = pokemon_dict["species"]
    init_dict["name"] = pokemon_dict["species"]
    init_dict["nature"] = pokemon_dict.get("nature", "serious")
    init_dict["item"] = pokemon_dict["item"]
    init_dict["gender"] = pokemon_dict["gender"]
    init_dict["ability"] = pokemon_dict["ability"]
    init_dict["evs"] = pokemon_dict.get("ev", {})
    init_dict["ivs"] = pokemon_dict.get("iv", {})
    init_dict["moves"] = pokemon_dict["moves"]

    return Pokemon(**init_dict)
