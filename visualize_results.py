"""Methods to visualize the results of simulations."""
import click
from log_manager.log_reader import LogReader

@click.command()
@click.option("-p",
              "--prefix",
              help="Prefix for files to select.")
def run(prefix):
    if prefix is None:
        raise RuntimeError("You must specify a prefix.")

    log_reader = LogReader(prefix=prefix)
    log_reader.read_data()
    



if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run()
