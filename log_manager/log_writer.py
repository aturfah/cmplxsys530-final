"""Log Manager Class."""
from os.path import join
from datetime import datetime

import config

class LogWriter():
    """Class for class that generates log files."""

    def __init__(self, prefix = None):
        """Initialize LogWriter for a simulation"""
        filename = join(config.LOG_DIR, generate_filename(prefix))
        print(filename)
        print("Init-ing logwriter")
    
    def __del__(self):
        """Delete LogWriter"""
        print("Deleting logwriter")

    def write_line(self):
        """Write line to this output"""
        pass


def generate_filename(prefix = None):
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

    filename = "{}{}/{}/{}_{}-{}-{}.csv".format(prefix_str, year, month, day, hour, minute, second)
    
    return filename