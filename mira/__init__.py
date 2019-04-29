"""Package mira is a Flask backend for the Mira application."""

import os

from flask import Flask
from flask_login.login_manager import LoginManager

app = Flask(
    "mira",
    root_path=os.getcwd(),
    template_folder="dist",
    static_folder="dist/static",
    instance_relative_config=True,
)

app.config.from_object("mira.default_config")
app.config.from_pyfile("application.cfg", silent=True)

LoginManager(app)

# In debug mode, enable cross-origin requests since we serve the Vue app on a
# different port for hot reloading.
if app.debug:
    from flask_cors import CORS

    CORS(app, with_credentials=True, resources={r"/api/*": {"origins": "*"}})


# In production, use SeaSurf for CSRF protection.
if not app.debug:
    from flask_seasurf import SeaSurf

    SeaSurf(app)

# In real production (Heroku), use Talisman to enforce https.
if not app.debug and "DYNO" in os.environ:
    from flask_talisman import Talisman

    Talisman(app)

import mira.views  # noqa
