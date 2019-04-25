"""Package mira is a Flask backend for the Mira application."""

import os

from flask import Flask
from flask_login.login_manager import LoginManager

app = Flask("mira", root_path=os.getcwd(), instance_relative_config=True)
LoginManager().init_app(app)

app.config.from_object("mira.default_config")
app.config.from_pyfile("application.cfg", silent=True)

import mira.views
