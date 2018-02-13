"""Log Manager Class."""
from os.path import join

from csv import writer

from datetime import datetime

import config


class LogWriter():
    """Class for class that generates log files."""

    def __init__(self, header, prefix=None):
        """Initialize LogWriter for a simulation.

        :param prefix: Prefix to lead filename with
        :param header: List as header row for file.
        """
        self.filename = generate_filename(prefix)
        self.output_file = generate_file(self.filename)
        self.output_csv = writer(self.output_file)

        self.header = header
        self.write_line(header)

    def __del__(self):
        """Delete LogWriter."""
        self.output_file.close()

    def write_line(self, dict_to_write):
        """Write line to this output.

        :param dict_to_write: Column Name/Value dict to write to file.
        """
        line = []
        self.output_csv.writerow(line)


def generate_filename(prefix):
    """Generate file for use in this LogWriter."""
    if not prefix:
        prefix_str = ""
    else:
        prefix_str = prefix + "_"

    now = datetime.now()
    day = "%02d" % now.day
    month = "%02d" % now.month
    year = now.year
    hour = "%02d" % now.hour
    minute = "%02d" % now.minute
    second = "%02d" % now.second

    filename = "{}{}-{}-{}_{}-{}-{}.csv".format(
        prefix_str, year, month, day, hour, minute, second)
    return filename


def generate_file(filename):
    """Generate the file that will be used."""
    file_ = join(config.LOG_DIR, filename)
    return open(file_, mode='w')
