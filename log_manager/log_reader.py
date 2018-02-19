"""Class for a log reader."""

from os import listdir
from os.path import isfile, join

from csv import reader

from math import inf

import config


class LogReader():
    """Log reader class."""

    def __init__(self, filename=None, prefix=None):
        """
        Init method for LogReader.

        One of filename or prefix should be specified,
        not both.

        :param filename: str
            String for filename to read.
        :param prefix: str
            Prefix for filenames to read.
        """
        if filename is None and prefix is None:
            raise AttributeError("One of filename or prefix must be specified")
        if filename is not None and prefix is not None:
            raise AttributeError("Only one of filename or\
                                 prefix can be specified")

        self.files = []
        if prefix is not None:
            for fname in listdir(config.LOG_DIR):
                full_fname = join(config.LOG_DIR, fname)
                if fname.startswith(prefix) and isfile(full_fname):
                    self.files.append(full_fname)
        else:
            self.files = [filename]

        if not self.files:
            raise AttributeError("No files match the prefix provided.")

        self.set_header()
        self.init_data()
        self.data_range = None

    def set_header(self):
        """Extract the header information from a file."""
        sample_filename = self.files[0]
        with open(sample_filename) as sample_file:
            csv_reader = reader(sample_file)
            header_row = next(csv_reader)
            self.header = header_row

    def init_data(self):
        """Initialize an empty list for each column."""
        self.data = {}
        for colname in self.header:
            self.data[colname] = []

    def read_data(self):
        """Populate the data."""
        for filename in self.files:
            file_ = open(filename)
            csv_reader = reader(file_)
            file_header = next(csv_reader)

            if file_header != self.header:
                # Invalid file, reset data
                self.init_data()
                raise RuntimeError(
                    "File {} has an invalid header".format(filename))
            for row in csv_reader:
                for col_index in range(len(self.header)):
                    self.data[self.header[col_index]].append(row[col_index])

            file_.close()

    def calc_data_range(self, columns):
        """Calculate the max/min values for the data."""
        max_val = -inf
        min_val = inf
        for column in columns:
            if column not in self.data:
                raise AttributeError("Invalid columns provided")

            for datum in self.data[column]:
                if datum < min_val:
                    min_val = datum
                if datum > max_val:
                    max_val = datum

        self.data_range = (min_val, max_val)

    def to_numeric(self, colnames):
        """Make the columns in colnames numeric data."""
        for colname in colnames:
            if colname not in self.header:
                raise AttributeError("Invalid column name: {}".format(colname))
            for datum in self.data[colname]:
                datum = float(datum)
