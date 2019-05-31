"""This module defines the data models for Mira."""

from base64 import b64encode
from datetime import datetime, timedelta
from io import BytesIO
from uuid import uuid4
import math
import re

from PIL import Image
from flask_login.mixins import UserMixin
from sqlalchemy import CheckConstraint, Column, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import (
    backref,
    deferred,
    joinedload,
    relationship,
    validates,
)
from sqlalchemy.types import Boolean, DateTime, Integer, LargeBinary, String
from werkzeug.security import generate_password_hash, check_password_hash

from mira.errors import InvalidAttribute
from mira.extensions import db


MIN_PASSWORD_LENGTH = 8
MAX_FRIENDS = 6

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9-_]+$")

SELF_STATE = "self"
FRIEND_STATE = "friend"
INCOMING_STATE = "incoming"
OUTGOING_STATE = "outgoing"
STRANGER_STATE = "stranger"

IMAGE_FORMAT = "PNG"
THUMBNAIL_SIZE = 100, 100
FADE_MULTIPLIER = 0.95
FADE_PERIOD = timedelta(hours=1)


class BaseModel(db.Model):
    """Base class for all models."""

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


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
        if not USERNAME_REGEX.match(value):
            raise InvalidAttribute(
                key, value, "Username contains invalid characters"
            )
        return value

    @classmethod
    def by_name(cls, username):
        """Look up a user by their username."""
        return cls.query.filter_by(username=username).first()

    def can_add_friend(self):
        """Return true if there is room for another friend."""
        return self.outgoing_friendships.count() < MAX_FRIENDS

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

    def serialize(self, state, friendship=None):
        """Serialize this user with additional data."""
        data = {"username": self.username, "state": state}
        if friendship:
            data["time"] = friendship.updated_at.isoformat() + "Z"
        if state == FRIEND_STATE:
            canvas = friendship.canvas
            thumbnail = canvas and canvas.thumbnail
            data["thumbnail"] = (
                b64encode(thumbnail).decode() if thumbnail else None
            )
        return data

    def friend_data(self, user):
        """Return data about a particular friend."""
        if self == user:
            return user.serialize(SELF_STATE)
        outgoing = (
            Friendship.between(self, user, query=True)
            .options(joinedload(Friendship.canvas).undefer(Canvas.thumbnail))
            .first()
        )
        incoming = (
            Friendship.between(user, self, query=True)
            .filter_by(ignored=False)
            .first()
        )
        if outgoing and incoming:
            return user.serialize(FRIEND_STATE, outgoing)
        if outgoing and not incoming:
            return user.serialize(OUTGOING_STATE, outgoing)
        if not outgoing and incoming:
            return user.serialize(INCOMING_STATE, incoming)
        return user.serialize(STRANGER_STATE)

    def all_friends_data(self):
        """Return data about all friends."""
        outgoing = self.outgoing_friendships.options(
            joinedload(Friendship.friendee),
            joinedload(Friendship.canvas).undefer(Canvas.thumbnail),
        )
        incoming = self.incoming_friendships.options(
            joinedload(Friendship.friender)
        ).filter_by(ignored=False)
        incoming_ids = {friendship.friender_id for friendship in incoming}
        friends = []
        only_outgoing = []
        only_incoming = []
        for friendship in outgoing:
            if friendship.friendee_id in incoming_ids:
                friends.append(
                    friendship.friendee.serialize(FRIEND_STATE, friendship)
                )
                incoming_ids.remove(friendship.friendee_id)
            else:
                only_outgoing.append(
                    friendship.friendee.serialize(OUTGOING_STATE, friendship)
                )
        for friendship in incoming:
            if friendship.friender_id in incoming_ids:
                only_incoming.append(
                    friendship.friender.serialize(INCOMING_STATE, friendship)
                )

        def by_username(record):
            return record["username"]

        friends.sort(key=by_username)
        only_outgoing.sort(key=by_username)
        only_incoming.sort(key=by_username)
        return friends + only_outgoing + only_incoming

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
    ignored = Column(Boolean, nullable=False, default=False)

    friender = relationship(
        "User",
        foreign_keys=[friender_id],
        backref=backref(
            "outgoing_friendships",
            lazy="dynamic",
            cascade="save-update, merge, delete",
        ),
    )
    friendee = relationship(
        "User",
        foreign_keys=[friendee_id],
        backref=backref(
            "incoming_friendships",
            lazy="dynamic",
            cascade="save-update, merge, delete",
        ),
    )
    canvas = relationship(
        "Canvas", backref="friendships", cascade="save-update, merge, delete"
    )

    def __init__(self, friender, friendee):
        self.friender_id = friender.id
        self.friendee_id = friendee.id

    @classmethod
    def between(cls, friender, friendee, query=False):
        """Return the friendship between two users, or None."""
        filtered = cls.query.filter_by(
            friender_id=friender.id, friendee_id=friendee.id
        )
        if query:
            return filtered
        return filtered.first()

    def __repr__(self):
        return f"<Friendship {self.friender_id},{self.friendee_id}>"


class Canvas(BaseModel):
    """A canvas shared between two friends."""

    __tablename__ = "canvases"

    id = Column(Integer, primary_key=True)
    thumbnail = deferred(Column(LargeBinary))
    data = deferred(Column(LargeBinary))
    last_fade = Column(DateTime)

    def mix(self, new_data):
        now = datetime.utcnow()
        if not self.data:
            self.data = new_data
            self.last_fade = now
            image = Image.open(BytesIO(new_data))
        else:
            image = Image.open(BytesIO(self.data))
            blank = image.copy()
            blank.putalpha(0)
            elapsed = now - self.last_fade
            if elapsed >= FADE_PERIOD:
                num_periods = math.floor(elapsed / FADE_PERIOD)
                alpha_multiplier = FADE_MULTIPLIER ** num_periods
                image = Image.blend(blank, image, alpha_multiplier)
                self.last_fade += num_periods * FADE_PERIOD
            new_image = Image.open(BytesIO(new_data))
            data_bytes = BytesIO()
            image.paste(new_image, (0, 0), mask=new_image)
            image.save(data_bytes, IMAGE_FORMAT)
            self.data = data_bytes.getvalue()
        thumbnail_bytes = BytesIO()
        image.thumbnail(THUMBNAIL_SIZE, Image.BICUBIC)
        image.save(thumbnail_bytes, IMAGE_FORMAT)
        self.thumbnail = thumbnail_bytes.getvalue()
        return self.data

    def __repr__(self):
        return f"<Canvas {self.id}>"
