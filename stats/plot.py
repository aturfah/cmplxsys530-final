"""Plotting some neat statistics from a ladder."""
from cycler import cycler

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

COLORS = ["b", "g", "r", "c", "m", "y", "k", "w"]


def plot_log_reader_data(log_reader):
    """Plot data from log_reader."""
    plt.subplots_adjust(right=0.8)
    plt.rc("axes", prop_cycle=(
        cycler("color", COLORS[:len(log_reader.header)])))

    legend_info = log_reader.header
    graph_dict = {}
    for group in log_reader.data:
        data_label = None
        for header_group in legend_info:
            if group.startswith(header_group):
                data_label = header_group
                break

        line_i, = plt.plot(log_reader.data[group], label=data_label, linewidth=0.75)
        graph_dict[group] = line_i

    plt.legend(legend_info, loc="upper left")
    plt.ylabel("Average Elo Ranking")

    def new_data(event):
        """Handle checkbox button click."""
        keys = graph_dict.keys()
        matching_vals = [val for val in keys if val.startswith(event)]
        for val in matching_vals:
            line = graph_dict[val]
            line.set_visible(not line.get_visible())
        plt.draw()

    change_axis = plt.axes([0.85, 0.65, 0.13, 0.2])
    change_buttons = CheckButtons(
        change_axis, legend_info, [True]*len(legend_info))

    change_buttons.on_clicked(new_data)
    plt.show()


def plot_matchup_matrix(colnames, matchup_matrix):
    """
    Plot matchup matrix as heatmap.

    Args:
        colnames (list): List of column names to display on heatmap; since
            matrix is NxN, also displays as rows.
        matchup_matrix (np.ndarray): 2xNxN Matrix of matchup results, where N
            is len(colnames)

    """
    plot1_data = matchup_matrix[0]
    plot2_data = matchup_matrix[1]

    wl_axis = plt.subplot(121)
    plt.title("W/L Ratio")
    plt.imshow(plot1_data, cmap="coolwarm")
    format_plot(wl_axis, colnames)

    num_games_axis = plt.subplot(122)
    plt.title("# of Games Played")
    plt.imshow(plot2_data, cmap="coolwarm")
    format_plot(num_games_axis, colnames)

    plt.show()


def format_plot(axis, colnames):
    """
    Do formatting for plots.

    Args:
        axis (plt.axis):  Plot figure with graph data.
        colnames (list): List of row/column names to display on heatmap.

    """
    num_rows = len(colnames)
    num_cols = len(colnames)

    plt.grid(which="minor", lw=1, color="black")

    axis.set_yticks([x for x in range(num_rows)])
    axis.set_xticks([x for x in range(num_cols)])
    axis.set_yticks([x - 0.5 for x in range(1, num_rows)], minor=True)
    axis.set_xticks([x - 0.5 for x in range(1, num_cols)], minor=True)
    axis.tick_params(axis="y", which="minor", bottom="off")
    axis.tick_params(axis="x", which="minor", bottom="off")
    axis.invert_yaxis()

    axis.set_xticklabels(colnames, minor=False)
    axis.set_yticklabels(colnames, minor=False)
    plt.xticks(rotation=45)

    plt.colorbar(orientation="horizontal", pad=0.25)
