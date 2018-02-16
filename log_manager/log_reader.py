"""Class for a log reader."""

import config

from os import listdir
from os.path import isfile, join

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
            raise AttributeError(
                "Only one of filename or prefix can be specified")

        if prefix is not None:
            for fname in listdir(config.LOG_DIR):
                full_fname = join(config.LOG_DIR, fname)
                if fname.startswith(prefix) and isfile(full_fname):
                    filename.append(fname)

        else:
            self.files = [filename]
