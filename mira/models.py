"""This module defines the data models for Mira."""

from uuid import uuid4

from flask_login.mixins import UserMixin
from sqlalchemy import CheckConstraint, Column, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.types import Boolean, DateTime, Integer, LargeBinary, String
from werkzeug.security import generate_password_hash, check_password_hash

from mira.errors import InvalidAttribute
from mira.extensions import db


MIN_PASSWORD_LENGTH = 8
MAX_FRIENDS = 5


class BaseModel(db.Model):
    """Base class for all models."""

    __abstract__ = True

    created_at = Column(DateTime, default=db.func.now())
    updated_at = Column(DateTime, default=db.func.now(), onupdate=db.func.now())


class User(BaseModel, UserMixin):
    """A user of Mira."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    pw_hash = Column(String, nullable=False)

    friendees = association_proxy("outgoing_friendships", "friendee")
    frienders = association_proxy("incoming_friendships", "friender")

    def __init__(self, username, password):
        """Create a new user."""
        self.username = username
        self.set_password(password)
        self.reset_login_id()

    def get_id(self):
        """Return the string ID used for Flask-Login."""
        return self.login_id

    def reset_login_id(self):
        """Change the login token to force the user to log in again."""
        self.login_id = str(uuid4())

    def set_password(self, password):
        """Reset the user's password (stores only the hash)."""
        if len(password) < MIN_PASSWORD_LENGTH:
            raise InvalidAttribute(
                "password",
                f"[string of length {len(password)}]",
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters",
            )
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the given password is correct."""
        return check_password_hash(self.pw_hash, password)

    @validates("username")
    def validate_username(self, key, value):
        if not value:
            raise InvalidAttribute(key, value, "Username must be nonempty")
        return value

    @classmethod
    def by_name(cls, username):
        """Look up a user by their username."""
        return cls.query.filter_by(username=username).first()

    def can_add_friend(self):
        """Return true if there is room for another friend."""
        return len(self.friendees) < MAX_FRIENDS

    def friends(self):
        """Return friends of this user."""
        ids = {user.id for user in self.frienders}
        return [user for user in self.friendees if user.id in ids]

    def incoming_friend_requests(self):
        """Return users from which this user has pending friend requests."""
        ids = {user.id for user in self.friendees}
        return [user for user in self.frienders if user.id not in ids]

    def outgoing_friend_requests(self):
        """Return users that have pending friend requests from this user."""
        ids = {user.id for user in self.frienders}
        return [user for user in self.friendees if user.id not in ids]

    def __eq__(self, other):
        # Don't do class check since current_user is a proxy object.
        return self.id == other.id

    def __repr__(self):
        return f"<User {self.username}>"


class Friendship(BaseModel):
    """A friendship between two users."""

    __tablename__ = "friendships"

    __table_args = (CheckConstraint("friender_id != friendee_id"),)

    friender_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    friendee_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    canvas_id = Column(Integer, ForeignKey("canvases.id", ondelete="SET NULL"))

    friender = relationship(
        "User",
        foreign_keys=[friender_id],
        backref=backref(
            "outgoing_friendships", cascade="save-update, merge, delete"
        ),
    )
    friendee = relationship(
        "User",
        foreign_keys=[friendee_id],
        backref=backref(
            "incoming_friendships", cascade="save-update, merge, delete"
        ),
    )
    canvas = relationship(
        "Canvas", backref="friendships", cascade="save-update, merge, delete"
    )

    def __init__(self, friender, friendee):
        self.friender_id = friender.id
        self.friendee_id = friendee.id

    @classmethod
    def between(cls, friender, friendee):
        """Return the friendship between two users, or None."""
        return cls.query.filter_by(
            friender_id=friender.id, friendee_id=friendee.id
        ).first()

    def __repr__(self):
        return f"<Friendship {self.friender_id},{self.friendee_id}>"


class Canvas(BaseModel):
    """A canvas shared between two friends."""

    __tablename__ = "canvases"

    id = Column(Integer, primary_key=True)
    thumbnail = Column(LargeBinary, nullable=True)
    data = Column(LargeBinary, nullable=True)

    def __repr__(self):
        return f"<Canvas {self.id}>"
