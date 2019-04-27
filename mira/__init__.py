"""Package mira is a Flask backend for the Mira application."""

import os

from flask import Flask
from flask_login.login_manager import LoginManager
from flask_seasurf import SeaSurf

app = Flask(
    "mira",
    root_path=os.getcwd(),
    template_folder="dist",
    static_folder="dist/static",
    instance_relative_config=True,
)

# First load default config, then instance/application.cfg.
app.config.from_object("mira.default_config")
app.config.from_pyfile("application.cfg", silent=True)

# Initialize the login manager and SeaSurf (CSRF protection).
LoginManager(app)
SeaSurf(app)

# In debug mode, enable cross-origin requests since we serve the Vue app
# separately (yarn run serve) for hot reloading.
if app.debug:
    from flask_cors import CORS

    CORS(app, with_credentials=True)

# In real production (Heroku), use Talisman to enforce https.
if app.env == "production" and "DYNO" in os.environ:
    from flask_talisman import Talisman

    Talisman(app)

import mira.views  # noqa
