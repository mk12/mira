"""This module defines the Flask views (routes) for the server."""

from flask import abort, jsonify, request

from mira import app
from mira.arguments import get_int
from mira.crud_helpers import (
    create,
    delete,
    get,
    paginate,
    update,
)
from mira.database import db
from mira.models import *


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, message=str(e)), 404


@app.route("/")
def index():
    return "Hello World!"


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return paginate(User, "created_at")
    elif request.method == "POST":
        return create(User, ["email", "name"])


@app.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def users_id(id):
    if request.method == "GET":
        return get(User, id)
    elif request.method == "PUT":
        return update(User, id, ["email", "name"])
    elif request.method == "DELETE":
        return delete(User, id)
