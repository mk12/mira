"""Package mira is a Flask back end for the Mira application."""

import os

from flask import Flask

from mira.config import get_config

app = Flask(
    "mira",
    root_path=os.getcwd(),
    template_folder="dist",
    static_folder="dist/static",
)

app.config.update(get_config(app.env))

import mira.extensions  # noqa
import mira.views  # noqa
