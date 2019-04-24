"""This module defines helper functions for extracting request arguments."""

from flask import abort, request


def get_int(name):
    """Get an integer from the query string."""
    value = request.args.get(name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        abort(404, "Query parameter '{}' is not an integer".format(name))


def get_json():
    """Get the request JSON, or abort 404 if it doesn't exist."""
    json = request.get_json()
    if not json:
        abort(404, "Expected JSON in request body")
    return json


def get_fields(model_name: str, required=None, permitted=None, provided=None):
    """Return input fields for a request."""
    required = required or []
    permitted = permitted or []
    provided = provided or {}
    fields = {}

    json = get_json()
    for f in required:
        value = json.get(f)
        if value is None:
            abort(404, "{} missing required attribute {}".format(model_name, f))
        else:
            fields[f] = value

    for f in permitted:
        value = json.get(f)
        if value is not None:
            fields[f] = value

    fields.update(provided)
    return fields
