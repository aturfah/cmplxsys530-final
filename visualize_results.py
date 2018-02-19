"""Methods to visualize the results of simulations."""
import click
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons


from log_manager.log_reader import LogReader
from stats import plot


@click.command()
@click.option("-p",
              "--prefix",
              help="Prefix for files to select.")
def run(prefix):
    if prefix is None:
        raise RuntimeError("You must specify a prefix.")

    log_reader = LogReader(prefix=prefix)
    log_reader.read_data()

    # print(log_reader.data)
    _, axis = plt.subplots()
    plt.subplots_adjust(right=0.8)
    legend_info = []
    graph_dict = {}

    for group in log_reader.data:
        line_i, = axis.plot(log_reader.data[group])
        legend_info.append(group)
        graph_dict[group] = line_i

    change_axis = plt.axes([0.85, 0.65, 0.13, 0.2])
    change_buttons = CheckButtons(
        change_axis, legend_info, [True]*len(legend_info))

    def new_data(event):
        """PEW."""
        line = graph_dict[event]
        line.set_visible(not line.get_visible())
        plt.draw()

    change_buttons.on_clicked(new_data)

    plt.show()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
