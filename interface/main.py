"""Main Flask App for Agent Interface"""

from flask import Flask
from flask import render_template

INTERFACE = Flask(__name__)

@INTERFACE.route("/")
def index():
    """Index page."""
    return render_template('index.html')
