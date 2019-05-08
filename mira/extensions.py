"""This module defines global Flask extensions."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login.login_manager import LoginManager
from flask_migrate import Migrate
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from mira import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
limiter = Limiter(app, key_func=get_remote_address)
talisman = Talisman(app, force_https=app.config["FORCE_HTTPS"])
sea_surf = SeaSurf(app)

if app.debug:
    # Enable cross-origin requests in debug mode, since we serve the Vue app on
    # a different port with webpack-dev-server.
    from flask_cors import CORS

    CORS(app, resources={r"/api/*": {"origins": "*"}})


    # Log all database queries in debug mode.
    import logging

    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
