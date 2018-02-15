"""Class for a log reader."""


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
