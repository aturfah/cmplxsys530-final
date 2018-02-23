"""Package to calculate interesting ladder metrics."""

import numpy as np


def calculate_avg_elo(ladder, group_by="type"):
    """
    Calculate the elo rankings on a ladder at a specific point in time.

    :param ladder: The ladder for which to calculate the rankings
    :param group_strategy: Whether to group results by
        strategy or by individuals
    """
    player_pool = ladder.get_players()
    output = {}

    for player in player_pool:
        if hasattr(player, group_by):
            player_strat = str(getattr(player, group_by))
            if player_strat not in output:
                output[player_strat] = []
            output[player_strat].append(player.elo)
        else:
            player_id = str(player.id)
            if player_id not in output:
                output[player_id] = []
            output[player_id].append(player.elo)

    for group in output:
        output[group] = sum(output[group])/len(output[group])

    return output


def calculate_matchups(log_reader):
    """Calculate matchup results for player types."""
    num_games = len(log_reader.data[log_reader.data_keys[0]])
    num_files = len(log_reader.files)

    results = {}

    for file_ind in range(num_files):
        outcome_key = "{}{}".format("outcome", file_ind)
        p1_type_key = "{}{}".format("player1.type", file_ind)
        p2_type_key = "{}{}".format("player2.type", file_ind)

        outcome_data = log_reader.data[outcome_key]
        p1_type_data = log_reader.data[p1_type_key]
        p2_type_data = log_reader.data[p2_type_key]
        for game_ind in range(num_games):
            outcome = outcome_data[game_ind]
            p1_type = p1_type_data[game_ind]
            p2_type = p2_type_data[game_ind]

            # Initialize the data for the types
            if p1_type not in results:
                results[p1_type] = {}
            if p2_type not in results:
                results[p2_type] = {}

            if p2_type not in results[p1_type]:
                results[p1_type][p2_type] = {}
                results[p1_type][p2_type]["wins"] = 0
                results[p1_type][p2_type]["total"] = 0
            if p1_type not in results[p2_type]:
                results[p2_type][p1_type] = {}
                results[p2_type][p1_type]["wins"] = 0
                results[p2_type][p1_type]["total"] = 0

            results[p1_type][p2_type]["total"] += 1
            results[p2_type][p1_type]["total"] += 1

            # Increment the counter of whoever won
            # (outcome+1)%2 turns 0 to 1 and 1 to 0
            results[p1_type][p2_type]["wins"] += outcome
            results[p2_type][p1_type]["wins"] += (outcome + 1) % 2

    results = calc_ratios(results)
    names, results = calculate_matchup_matrix(results)
    return names, results


def calc_ratios(results):
    """Calculate the ratios for a given results dict."""
    for p1_type in results:
        for p2_type in results[p1_type]:
            num_wins = results[p1_type][p2_type]["wins"]
            num_total = results[p1_type][p2_type]["total"]
            if num_total != 0:
                results[p1_type][p2_type]["ratio"] = num_wins/num_total
            else:
                results[p1_type][p2_type]["ratio"] = None

    return results


def calculate_matchup_matrix(results):
    """From the results of calc_matchups(), calculate matchups as matrix"""
    names = list(results.keys())
    num_cols = len(names)

    output = np.zeros((2, num_cols, num_cols))

    # Generate matchup matrix
    for col_ind in range(num_cols):
        for row_ind in range(num_cols):
            rowname = names[row_ind]
            colname = names[col_ind]

            output[0, row_ind, col_ind] = results[rowname][colname]["ratio"]
            output[1, row_ind, col_ind] = results[rowname][colname]["total"]

    return names, output
