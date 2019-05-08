"""This module configures Flask based on defaults and environment variables."""

import os

from dotenv import load_dotenv


# Load environment variables from the .env file.
load_dotenv()


ENVIRONMENTS = ["development", "production"]

DEFAULT_CONFIG = {
    "base": {
        # Disable this because it reduces performance and we don't need it.
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        # We should never need to read cookies from JavaScript.
        "CSRF_COOKIE_HTTPONLY": True,
        "REMEMBER_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_HTTPONLY": True,
    },
    "development": {
        "FORCE_HTTPS": False,
        # We can't render CSRF tokens in development since the web pages are
        # served by webpack-dev-server (for hot reloading), not by Flask.
        "CSRF_DISABLE": True,
    },
    "production": {
        # Make sure we use HTTPS for everything in production.
        "FORCE_HTTPS": True,
        "SESSION_COOKIE_SECURE": True,
        "REMEMBER_COOKIE_SECURE": True,
        "CSRF_COOKIE_SECURE": True,
    },
}


def get_config(env):
    """Get the configuration for a given environment."""
    if env not in ENVIRONMENTS:
        raise ValueError(f"Unsupported environment: {env}")
    return {
        **DEFAULT_CONFIG["base"],
        **DEFAULT_CONFIG[env],
        **get_user_config(),
    }


def get_user_config():
    """Get the user configuration from environment variables."""
    https = getenv("FLASK_FORCE_HTTPS", parse=parse_bool)
    config = {
        "FORCE_HTTPS": https,
        "SESSION_COOKIE_SECURE": https,
        "REMEMBER_COOKIE_SECURE": https,
        "CSRF_COOKIE_SECURE": https,
        "RATELIMIT_ENABLED": getenv(
            "FLASK_RATELIMIT_ENABLED", parse=parse_bool
        ),
        "SECRET_KEY": getenv("FLASK_SECRET_KEY", required=True),
        "SQLALCHEMY_DATABASE_URI": getenv("DATABASE_URL", required=True),
    }
    return {k: v for k, v in config.items() if v is not None}


def getenv(name, required=False, parse=None):
    """Get an environment variable."""
    value = os.getenv(name)
    if required and value is None:
        raise ValueError(f"Environment variable not found: {name}")
    if parse is not None and value is not None:
        value = parse(name, value)
    return value


def parse_bool(name, value):
    """Parse an environment variable value as a boolean."""
    value = value.lower()
    if value in ("false", "off", "no", "0"):
        return False
    if value in ("true", "on", "yes", "1"):
        return True
    raise ValueError(f"Invalid boolean environment variable: {name}={value}")
