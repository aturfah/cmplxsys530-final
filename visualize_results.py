"""Methods to visualize the results of simulations."""
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

import click

from log_manager.log_reader import LogReader
from stats import plot


@click.command()
@click.option("-p",
              "--prefix",
              help="Prefix for files to select.")
def run(prefix):
    """PEW."""
    filenames = None
    if prefix is None:
        root = Tk()
        root.withdraw()
        root.update()
        filenames = askopenfilenames()
        root.destroy()
        if not filenames:
            raise RuntimeError("You must specify a prefix or select files.")

    log_reader = LogReader(prefix=prefix, filenames=filenames)
    log_reader.read_data()
    log_reader.to_numeric(log_reader.data_keys)

    plot.plot_log_reader_data(log_reader)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
