"""This module defines the Flask views (routes) for the server."""

from flask import jsonify, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import HTTPException, InternalServerError

from mira import app
from mira.arguments import get_fields
from mira.models import User


@app.errorhandler(HTTPException)
def handle_http_error(ex):
    # For a 500 Internal Server Error, Flask passes the original exception. We
    # don't want that as the exception message could have sensitive inforation.
    # https://github.com/pallets/flask/issues/2778
    if not isinstance(ex, HTTPException):
        ex = InternalServerError()
    return jsonify(error=ex.code, message=str(ex)), ex.code


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(login_id=user_id).first()


@app.route("/api/ping", methods=["POST"])
def ping():
    return "pong"


@app.route("/api/login", methods=["POST"])
def login():
    username, password = get_fields("username", "password")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return "Login failed", 401
    login_user(user, remember=True)
    user = current_user
    assert user.is_authenticated
    return "Logged in"


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return "Logged out"


@app.route("/api/user")
@login_required
def user_info():
    user = current_user
    return jsonify(username=user.username, color=user.color)


@app.route("/api/sync", methods=["POST"])
@login_required
def sync():
    pass


@app.route("/api/history")
@login_required
def history():
    pass
