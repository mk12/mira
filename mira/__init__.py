"""Package mira is a Flask backend for the Mira application."""

from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("mira.default_config")
app.config.from_pyfile("application.cfg", silent=True)

import mira.views
