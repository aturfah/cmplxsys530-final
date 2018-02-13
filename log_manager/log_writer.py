"""Log Manager Class."""
from os.path import join

from csv import writer

from datetime import datetime

import config


class LogWriter():
    """Class for class that generates log files."""

    def __init__(self, prefix=None):
        """Initialize LogWriter for a simulation."""
        self.output_file = generate_file(prefix)
        self.output_csv = writer(self.output_file)

    def __del__(self):
        """Delete LogWriter."""
        self.output_file.close()

    def write_line(self):
        """Write line to this output."""
        self.output_csv.writerow(['pew', 'test', 'pew'])


def generate_file(prefix=None):
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

    filename = join(config.LOG_DIR, filename)
    return open(filename, mode='w')
