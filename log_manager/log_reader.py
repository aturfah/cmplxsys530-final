"""Class for a log reader."""

from os import listdir
from os.path import isfile, join

from csv import reader

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
        self.generate_data_keys()
        self.init_data()

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
        for colname in self.data_keys:
            self.data[colname] = []

    def generate_data_keys(self):
        """Generate list of keys for for self.data."""
        keys = []
        for index in range(len(self.files)):
            file_columns = ["{}{}".format(colname, index)
                            for colname in self.header]
            keys.extend(file_columns)
        self.data_keys = keys

    def read_data(self):
        """Populate the data."""
        index = 0
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
                    key_name = "{}{}".format(self.header[col_index], index)
                    self.data[key_name].append(row[col_index])

            index += 1
            file_.close()

    def to_numeric(self, colnames):
        """Make the columns in colnames numeric data."""
        for colname in colnames:
            if colname not in self.data_keys:
                raise AttributeError("Invalid column name: {}".format(colname))
            self.data[colname] = [float(datum) for datum in self.data[colname]]
