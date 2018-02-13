"""Unit tests for LogWriter."""
from log_manager.log_writer import LogWriter


def test_basic():
    """Basic test for LogWriter class."""
    header = ["test1", "test2", "test3"]
    lw1 = LogWriter(header=header, prefix="test")

    dict_to_write = {}
    dict_to_write["test1"] = "pew"
    dict_to_write["test2"] = "foo"
    dict_to_write["test3"] = "bar"

    lw1.write_line(dict_to_write)

def test_prefix_handling():
    """Test prefix validation for LogWriter."""
    # Test for invalid characters (in this case tab)
    catch_err_1 = False
    try:
        _ = LogWriter(header=[], prefix="\test")
    except AttributeError:
        catch_err_1 = True

    assert catch_err_1

test_basic()
test_prefix_handling()
