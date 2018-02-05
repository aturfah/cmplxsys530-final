""" Plotting some neat statistics from a ladder """

import matplotlib.pyplot as plt


def plot_group_ratings(data):
    print("plotting data...")
    legend_info = []

    for group in data:
        plt.plot(data[group])
        legend_info.append(group)

    plt.legend(legend_info, loc='upper left')
    plt.show()
