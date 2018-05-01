"""Log Manager Class."""
from os.path import join

from csv import writer

from datetime import datetime

import config


class LogWriter():
    """
    Class for class that generates log files.

    Attributes:
        filename (str): Name of the log file.
        output_file (file): File stream of the log file.
        output_csv (writer): CSV writer for the log file.
        header (list): List of columns in this csv file.

    """

    def __init__(self, header, prefix=None):
        """Initialize LogWriter for a simulation.

        Args:
            prefix (str): Optional prefix to lead filename with.
            header (list): List with column names. Also defines first
                row in the output file.

        """
        # Invalid prefix name check
        if prefix is not None:
            invalid_char_seqs = ["/", "\\", "."]
            for char_seq in invalid_char_seqs:
                if char_seq in repr(prefix):
                    raise AttributeError("Prefix cannot contain slashes")

        # Validate header actually has content
        if not header:
            raise AttributeError("Header cannot be empty")

        self.filename = generate_filename(prefix)
        self.output_file = generate_file(self.filename)
        self.output_csv = writer(self.output_file)

        self.header = header
        self.output_csv.writerow(header)

    def __del__(self):
        """Delete LogWriter."""
        if hasattr(self, "output_file"):
            self.output_file.flush()
            self.output_file.close()

    def write_line(self, dict_to_write):
        """Write line to this output.

        Args:
            dict_to_write (dict): Information to write to file.
                Keys should be column names.

        """
        line = []

        for col_name in self.header:
            if col_name in dict_to_write:
                line.append(dict_to_write[col_name])
            else:
                line.append("NA")

        self.output_csv.writerow(line)


def generate_filename(prefix):
    """
    Generate file for use in this LogWriter.

    Args:
        prefix (str): Prefix for the file name.

    """
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
    microsecond = "%02d" % now.microsecond

    filename = "{}{}-{}-{}_{}-{}-{}-{}.csv".format(
        prefix_str, year, month, day, hour, minute, second, microsecond)
    return filename


def generate_file(filename):
    """
    Generate the file that will be used.

    Args:
        filename (str): Name of the file to be created.

    Returns:
        File object with the name <filename>.

    """
    file_ = join(config.LOG_DIR, filename)
    return open(file_, mode="w", newline="")
