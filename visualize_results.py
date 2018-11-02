"""Methods to visualize the results of simulations."""
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

import click

from file_manager.log_reader import LogReader
from stats import plot
from stats import calc


@click.command()
@click.option("-p",
              "--prefix",
              help="Prefix for files to select.")
@click.option("-m",
              "--method",
              help="What type of visualization to do.")
@click.argument("numeric_columns", nargs=-1)
def run(prefix, method, numeric_columns):
    """
    Visualize the data from a LogReader.

    Args:
        prefix (str): Prefix to specify for LogReader's files.
        numeric_columns (tuple): Which columns to convert to numeric (for the analysis)

    """
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

    if method == "elo":
        if numeric_columns == ():
            log_reader.to_numeric(log_reader.data_keys)
        else:
            num_col_keys = log_reader.to_data_key(numeric_columns)
            log_reader.to_numeric(num_col_keys)

        plot.plot_log_reader_data(log_reader)

    elif method == "matchups":
        num_col_keys = None
        if numeric_columns == ():
            num_col_keys = log_reader.to_data_key(
                ["player1.elo", "player2.elo", "outcome"])
            log_reader.to_numeric(num_col_keys)
        else:
            num_col_keys = log_reader.to_data_key(numeric_columns)
            log_reader.to_numeric(num_col_keys)

        results = calc.calculate_matchups(log_reader)
        colnames, matchup_matrix = calc.calculate_matchup_matrix(results)

        plot.plot_matchup_matrix(colnames, matchup_matrix)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
