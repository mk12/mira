"""This module defines the data models for Mira."""

from uuid import uuid4

from flask_login.mixins import UserMixin
from sqlalchemy import Column, DateTime, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from mira.database import db


class User(db.Model, UserMixin):
    """A user of Mira."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    pw_hash = Column(String, nullable=False)
    color = Column(String, nullable=False)

    created_at = Column(DateTime, default=db.func.now())
    updated_at = Column(DateTime, default=db.func.now(), onupdate=db.func.now())

    def get_id(self):
        """Return the string ID used for Flask-Login."""
        return self.login_id

    def reset_login_id(self):
        """Change the login token to force the user to log in again."""
        self.login_id = str(uuid4())

    def set_password(self, password):
        """Reset the user's password (stores only the hash)."""
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the given password is correct."""
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return f"<User #{self.id} {self.username}>"
