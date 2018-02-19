"""Plotting some neat statistics from a ladder."""
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

from stats.calc import calculate_data_range

def plot_group_ratings(data):
    """Plot the data broken down by groups."""
    print("plotting data...")
    legend_info = []

    for group in data:
        plt.plot(data[group])
        legend_info.append(group)

    plt.legend(legend_info, loc='upper left')
    plt.show()

def plot_log_reader_data(log_reader):
    data_range = calculate_data_range(log_reader)

    plt.subplots_adjust(right=0.8)
    legend_info = []
    graph_dict = {}
    for group in log_reader.data:
        legend_info.append(group)
        line_i, = plt.plot(log_reader.data[group], label=group)
        graph_dict[group] = line_i

    plt.legend(legend_info, loc='upper left')
    plt.ylabel("Average Elo Ranking")
    plt.ylim(data_range[0], data_range[1])

    def new_data(event):
        """PEW."""
        line = graph_dict[event]
        line.set_visible(not line.get_visible())
        plt.draw()

    change_axis = plt.axes([0.85, 0.65, 0.13, 0.2])
    change_buttons = CheckButtons(
        change_axis, legend_info, [True]*len(legend_info))

    change_buttons.on_clicked(new_data)
    plt.show()