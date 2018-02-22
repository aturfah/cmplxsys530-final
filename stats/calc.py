"""Package to calculate interesting ladder metrics."""


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

def calculate_matchups(log_reader, stratify=False):
    """Calculate matchup results for player types."""
    num_games = len(log_reader.data[log_reader.data_keys[0]])
    results_dict = {}

    outcome_cols = []
    type_cols = []
    elo_cols = []

    num_files = len(outcome_cols)

    for key_name in log_reader.data_keys:
        if "outcome" in key_name:
            outcome_cols.append(key_name)
        elif ".type" in key_name:
            type_cols.append(key_name)
        elif ".elo" in key_name:
            elo_cols.append(key_name)

    print(outcome_cols)
    print(type_cols)
    print(elo_cols)

    for game_ind in range(num_games):
        for file_ind in range(num_files):
            pass
