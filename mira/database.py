"""This module configures the SQLAlchemy database engine."""

import os

from flask_sqlalchemy import SQLAlchemy

from mira import app


def get_database_uri():
    """Get the database URI from the environment or configuration files."""
    uri = os.environ.get("DATABASE_URL")
    if uri:
        return uri
    uri = "{dialect}+{driver}://{user}:{password}@{host}/{dbname}"
    return uri.format(
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        **app.config["DB_CONNECTION"]
    )


def is_db_running():
    """Return true if the database connection is working."""
    try:
        db.session.execute("SELECT 1")
    except Exception:
        return False
    return True


app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
db = SQLAlchemy(app)
