"""Methods to visualize the results of simulations."""
import click
import numpy as np

import matplotlib.pyplot as plt

from log_manager.log_reader import LogReader
from stats import plot
from stats import calc


@click.command()
@click.option("-p",
              "--prefix",
              help="Prefix for files to select.")
def run(prefix):
    """PEW."""
    if prefix is None:
        raise RuntimeError("You must specify a prefix.")

    log_reader = LogReader(prefix=prefix)
    log_reader.read_data()
    log_reader.to_numeric(log_reader.header)

    plot.plot_log_reader_data(log_reader)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
