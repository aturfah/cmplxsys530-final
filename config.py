"""Config file with directory info."""
import os

# Log file directory
LOG_DIR = "logs/"
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)
