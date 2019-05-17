"""This module defines global Flask extensions."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login.login_manager import LoginManager
from flask_migrate import Migrate
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from mira import app


CONTENT_SECURITY_POLICY = {
    "default-src": "'self'",
    "script-src": "'self'",
    # Allow base64-encoded image data.
    "img-src": "'self' data:",
    # Allow fonts from Google Fonts.
    "font-src": "'self' *.gstatic.com",
    "style-src": "'self' fonts.googleapis.com *.gstatic.com",
}


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
limiter = Limiter(app, key_func=get_remote_address)
csrf = SeaSurf(app)
talisman = Talisman(
    app,
    force_https=app.config["FORCE_HTTPS"],
    session_cookie_secure=app.config["SESSION_COOKIE_SECURE"],
    content_security_policy=CONTENT_SECURITY_POLICY,
    content_security_policy_nonce_in=["script-src"],
)

if app.debug:
    # Enable cross-origin requests in debug mode, since we serve the Vue app on
    # a different port with webpack-dev-server.
    from flask_cors import CORS

    CORS(
        app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}}
    )

    # Log all database queries in debug mode.
    import logging

    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
