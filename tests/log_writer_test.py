"""Unit tests for LogWriter."""
from log_manager.log_writer import LogWriter


def test_basic():
    """Basic test for LogWriter class."""
    lw1 = LogWriter(prefix="test")
    lw1.write_line()


test_basic()
