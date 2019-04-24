"""This module defines the data models for Mira."""

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import joinedload, validates

from mira.database import db
from mira.errors import InvalidAttribute


# Double-precision floating-point type.
Double = Float(precision=53)


class BaseModel(db.Model):
    """Base class for all models."""

    __abstract__ = True

    created_at = Column(DateTime, default=db.func.now())
    updated_at = Column(DateTime, default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def relations(cls):
        """Return a mapping from names to relation objects.

        This maps singular names to relation objects that are on the "one" side
        of a one-to-many relationship. For example, if there is one User for
        each Comment, then the Comment relations method should map 'user' to
        that User relation object designating a unique user, and the User
        relations method should not mention Comment at all.
        """
        return {}

    def serialize(self):
        """Serialize the model to a dict."""
        raise NotImplementedError()

    def before_commit(self):
        """Hook that is run before insert and before update."""
        self.process()

    def after_commit(self):
        """Hook that is run after insert and after update."""
        self.put_to_es()

    def before_delete(self):
        """Hook that is run before delete."""

    def after_delete(self):
        """Hook that is run after delete."""
        self.delete_from_es()

    def process(self):
        """Process the model before committing it in the database."""


@db.event.listens_for(BaseModel, ("before_insert"), propagate=True)
@db.event.listens_for(BaseModel, ("before_update"), propagate=True)
def before_commit(mapper, connect, target):
    target.before_commit()


@db.event.listens_for(BaseModel, ("after_insert"), propagate=True)
@db.event.listens_for(BaseModel, ("after_update"), propagate=True)
def after_commit(mapper, connect, target):
    target.after_commit()


@db.event.listens_for(BaseModel, ("before_delete"), propagate=True)
def before_delete(mapper, connect, target):
    target.before_delete()


@db.event.listens_for(BaseModel, ("after_delete"), propagate=True)
def after_delete(mapper, connect, target):
    target.after_delete()


class User(BaseModel):
    """A user of Mira."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)

    def serialize(self):
        return {"id": self.id, "email": self.email, "name": self.name}

    def __repr__(self):
        return "<User #{} {}>".format(self.id, self.email)
