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
@click.option("-m",
              "--method",
              help="What to do with the files.")
@click.argument("numeric_columns", nargs=-1)
def run(prefix, method, numeric_columns):
    """Visualize the data from a LogReader."""
    if method is None:
        raise RuntimeError("No method specified.")

    filenames = None
    if prefix is None:
        # Hide TK Window
        root = Tk()
        root.withdraw()
        root.update()
        filenames = askopenfilenames()
        root.destroy()

        # Cancelled file load
        if not filenames:
            raise RuntimeError("You must specify a prefix or select files.")

    # Initialize LogReader with files/prefix
    log_reader = LogReader(prefix=prefix, filenames=filenames)
    log_reader.read_data()

    if method == "graph":
        if numeric_columns == ():
            log_reader.to_numeric(log_reader.data_keys)
        else:
            log_reader.to_numeric(numeric_columns)

        plot.plot_log_reader_data(log_reader)



if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
