"""Package to calculate interesting ladder metrics."""

from math import inf

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

def calculate_data_range(log_reader, columns):
    """Calculate the max/min values for the data."""
    max_val = -inf
    min_val = inf
    for column in columns:
        if column not in log_reader.data:
            raise AttributeError("Invalid columns provided")

        for datum in log_reader.data[column]:
            if datum < min_val:
                min_val = datum
            if datum > max_val:
                max_val = datum

    return (min_val, max_val+1)