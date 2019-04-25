"""This module defines helper functions for extracting request arguments."""

from flask import abort, request


def get_json():
    """Get the request JSON, or abort 404 if it doesn't exist."""
    if not request.json:
        abort(400, "Expected JSON in request body")
    return request.json


def get_fields(*keys):
    """Return input fields for a request."""
    json = get_json()
    for f in keys:
        if f not in json:
            abort(400, f"Missing required key: {f}")
    for key, val in json.items():
        if key not in keys:
            abort(400, f"Unexpected key: {f}")
    return [json[f] for f in keys]
