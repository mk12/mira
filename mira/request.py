"""This module provides helper functions for servicing requests."""

from flask import Request, abort, jsonify, request


def ok(code, message, **kwargs):
    """Create a JSON success response."""
    return jsonify(code=code, message=message, **kwargs)


def error(status, code, message, **kwargs):
    """Create a JSON error response."""
    return jsonify(code=code, message=message, **kwargs), status


def abort_json(status, code, message, **kwargs):
    """Abort with a JSON error response."""
    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = status
    abort(response)


def on_json_loading_failed(request, error):
    """Callback for when JSON parsing fails."""
    abort_json(400, "invalid_json", "Problems parsing JSON")


Request.on_json_loading_failed = on_json_loading_failed


def get_json(required=None, permitted=None):
    """Get validated JSON from the request body."""
    required = required or []
    permitted = permitted or []
    if not request.is_json:
        abort_json(415, "invalid_format", "Request body should be JSON")
    json = request.get_json()
    all_permitted = set().union(required, permitted)
    unexpected_fields = [key for key in json.keys() if key not in all_permitted]
    if unexpected_fields:
        abort_json(
            400,
            "unexpected_fields",
            "Request included unexpected fields",
            fields=unexpected_fields,
        )
    missing_fields = [key for key in required if key not in json]
    if missing_fields:
        abort_json(
            400,
            "missing_fields",
            "Request is missing required fields",
            fields=missing_fields,
        )
    return json


def get_fields(*fields):
    """Get the input fields for a request."""
    json = get_json(fields)
    if len(fields) == 1:
        return json[fields[0]]
    return [str(json[f]) for f in fields]
