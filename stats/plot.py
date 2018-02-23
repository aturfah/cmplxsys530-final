"""Plotting some neat statistics from a ladder."""
from cycler import cycler

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

import numpy as np

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

        line_i, = plt.plot(log_reader.data[group], label=data_label)
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
    """Plot matchup matrix as heatmap."""
    plot1_data = matchup_matrix[0,:,:]
    plot2_data = matchup_matrix[1,:,:]

    
    ax = plt.subplot(121)
    plt.title("W/L Ratio")
    plt.imshow(plot1_data, cmap="coolwarm")
    plt.grid(which="minor", lw=1, color="black")

    ax.set_yticks(np.arange(plot1_data.shape[0]))
    ax.set_xticks(np.arange(plot1_data.shape[1]))
    ax.set_yticks([x - 0.5 for x in np.arange(1, plot1_data.shape[1])], minor=True)
    ax.set_xticks([x - 0.5 for x in np.arange(1, plot1_data.shape[1])], minor=True)
    ax.tick_params(axis="y",which="minor",bottom="off")
    ax.tick_params(axis="x",which="minor",bottom="off")
    ax.invert_yaxis()

    ax.set_xticklabels(colnames, minor=False)
    ax.set_yticklabels(colnames, minor=False)
    plt.xticks(rotation=45)
    
    plt.colorbar()


    plt.subplot(122)
    plt.title("# of Games Played")
    plt.imshow(plot2_data, cmap="coolwarm")
    
    plt.colorbar()

    plt.show()