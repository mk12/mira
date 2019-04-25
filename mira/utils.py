"""This module defines general utilities."""

from mira.database import db
from mira.models import User


def create_user(username, password, color):
    """Create a new user in the database."""
    user = User(username=username, color=color)
    user.reset_login_id()
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
