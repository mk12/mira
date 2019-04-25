"""This module defines the Flask views (routes) for the server."""

from flask import jsonify, request, render_template, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.exceptions import HTTPException

from mira import app
from mira.arguments import get_fields
from mira.models import User


@app.errorhandler(HTTPException)
def http_error(ex):
    if request.path.startswith("/api/"):
        return jsonify(error=ex.code, message=str(ex)), ex.code
    content = {"heading": f"{ex.code} {ex.name}", "message": ex.description}
    return render_template("error.html", **content), ex.code


@app.route("/")
def index():
    return render_template("index.html")


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(login_id=user_id).first()


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
def ping():
    user = current_user
    return jsonify(username=user.username, color=user.color)
