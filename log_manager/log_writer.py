"""Log Manager Class."""
from os.path import join

from csv import writer

from datetime import datetime

import config


class LogWriter():
    """Class for class that generates log files."""

    def __init__(self, prefix=None, header=None):
        """Initialize LogWriter for a simulation."""
        self.filename = generate_filename(prefix)
        self.output_file = generate_file(self.filename)
        self.output_csv = writer(self.output_file)
        
        self.header = header
        if header:
            self.write_line(header)

    def __del__(self):
        """Delete LogWriter."""
        self.output_file.close()

    def write_line(self, line):
        """Write line to this output."""
        if self.header:
            pass
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
