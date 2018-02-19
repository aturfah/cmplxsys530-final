"""Plotting some neat statistics from a ladder."""
from cycler import cycler

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

COLORS = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def plot_log_reader_data(log_reader):
    """Plot data from log_reader."""

    plt.subplots_adjust(right=0.8)
    plt.rc('axes', prop_cycle=(
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

    plt.legend(legend_info, loc='upper left')
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
