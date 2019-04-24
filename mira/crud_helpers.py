"""This module defines helper functions for CRUD operations."""

from typing import Sequence, Type

from flask import abort, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from mira.arguments import get_fields, get_int
from mira.database import db
from mira.errors import InvalidAttribute
from mira.models import BaseModel


def get_or_404(model: Type[BaseModel], id: int):
    """Get a model object by ID, and 404 if it doesn't exist."""
    object = model.get(id)
    if not object:
        abort(404, "{} with ID {} does not exist".format(model.__name__, id))
    return object


def paginate(model: Type[BaseModel], order: str, **provided) -> str:
    """List resource items in a paginated fashion."""
    results = model.filter_by(**provided).order_by(order)

    page = get_int("page")
    per_page = get_int("per_page")
    if page is not None and per_page is not None:
        results = results.paginate(page, per_page)
        return jsonify(
            page=results.page,
            total_pages=results.pages,
            total_results=results.total,
            items=[item.serialize() for item in results.items],
        )

    # By default, return all items.
    items = [item.serialize() for item in results]
    return jsonify(page=1, total_pages=1, total_results=len(items), items=items)


def create(
    model: Type[BaseModel],
    required: Sequence[str],
    permitted: Sequence[str] = None,
    **provided
) -> str:
    """Create a new resource item."""
    fields = get_fields(model.__name__, required, permitted, provided)
    try:
        object = model(**fields)
        db.session.add(object)
        db.session.commit()
    except IntegrityError as e:
        abort(404, "Integrity error: {}".format(e))
    except InvalidAttribute as e:
        abort(404, e)
    return jsonify(object.serialize())


def get(model: Type[BaseModel], id: int) -> str:
    """Get an existing resource item."""
    return jsonify(get_or_404(model, id).serialize())


def update(model: Type[BaseModel], id: int, permitted: Sequence[str]) -> str:
    """Update an existing resource item."""
    fields = get_fields(model.__name__, permitted=permitted)
    object = get_or_404(model, id)
    try:
        for k, v in fields.items():
            setattr(object, k, v)
        db.session.commit()
    except InvalidAttribute as e:
        abort(404, e)
    return "OK"


def delete(model: Type[BaseModel], id: int) -> str:
    """Delete a resource item."""
    object = get_or_404(model, id)
    db.session.delete(object)
    db.session.commit()
    return "OK"
