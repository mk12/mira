"""This module defines views, including both web routes and API endpoints."""

from base64 import b64encode

from flask import jsonify, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, InternalServerError

from mira import app
from mira.errors import InvalidAttribute
from mira.extensions import db, limiter, login_manager
from mira.models import Canvas, Friendship, User
from mira.request import error, get_fields, ok


# Rate limits for API endpoints.
public_limit = limiter.shared_limit("10/minute", scope="public")
username_limit = limiter.limit(
    "30/minute",
    key_func=lambda: request.json["username"],
    exempt_when=lambda: not request.json or not request.json.get("username"),
)
logged_in_limit = limiter.limit("60/minute")


@app.errorhandler(HTTPException)
def handle_http_error(ex):
    # For a 500 Internal Server Error, Flask passes the original exception. We
    # don't want that as the exception message could have sensitive inforation.
    # https://github.com/pallets/flask/issues/2778
    if not isinstance(ex, HTTPException):
        ex = InternalServerError()
    return error(ex.code, "error", ex.name)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    username = current_user.username if current_user.is_authenticated else None
    return render_template("index.html", username=username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(login_id=user_id).first()


@app.route("/api/check")
@login_required
@logged_in_limit
def check():
    return ok("logged_in", "You are logged in", username=current_user.username)


@app.route("/api/login", methods=["POST"])
@public_limit
@username_limit
def login():
    username, password = get_fields("username", "password")
    user = User.by_name(username)
    if not user or not user.check_password(password):
        return error(401, "login_fail", "Wrong username or password")
    login_user(user, remember=True)
    assert current_user.is_authenticated
    return ok("login", "Logged in")


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return ok("logout", "Logged out")


@app.route("/api/register", methods=["POST"])
@public_limit
def register():
    username, password = get_fields("username", "password")
    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    except InvalidAttribute as ex:
        return error(422, "invalid_field", ex.message, field=ex.attribute)
    except IntegrityError:
        return error(
            409,
            "username_taken",
            "The username is already taken",
            username=username,
        )
    return ok("register", "Registered account")


@app.route("/api/change_password", methods=["PUT"])
@login_required
@logged_in_limit
def change_password():
    password, new_password = get_fields("password", "new_password")
    user = current_user
    if not user.check_password(password):
        return error(401, "auth_fail", "Wrong password")
    user.set_password(new_password)
    user.reset_login_id()
    db.session.add(user)
    db.session.commit()
    logout_user()
    return ok("change", "Changed password and logged out")


@app.route("/api/account", methods=["DELETE"])
@login_required
@logged_in_limit
def delete_user():
    password = get_fields("password")
    user = current_user
    if not user.check_password(password):
        return error(401, "auth_fail", "Wrong password")
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return ok("delete", "Deleted account")


@app.route("/api/friends/<username>")
@login_required
@logged_in_limit
def get_friend(username):
    user = User.by_name(username)
    if not user:
        return error(404, "unknown_user", "No user has that username")
    return jsonify(current_user.friend_data(user))


@app.route("/api/friends/<username>", methods=["PUT"])
@login_required
@logged_in_limit
def add_friend(username):
    user = User.by_name(username)
    if not user:
        return error(404, "unknown_user", "No user has that username")
    if user == current_user:
        return error(422, "self", "Self cannot be a friend")
    friendship = Friendship.between(current_user, user)
    reverse_friendship = Friendship.between(user, current_user)
    if friendship:
        if reverse_friendship:
            return ok("no_op_accept", "Already friends")
        if friendship.ignored:
            friendship.ignored = False
            db.session.add(friendship)
            db.session.commit()
            return ok("request", "Sent friend request")
        return ok("no_op_request", "Already sent friend request")
    if not current_user.can_add_friend():
        return error(422, "maximum", "Cannot add more friends")
    friendship = Friendship(current_user, user)
    if reverse_friendship:
        canvas = Canvas()
        friendship.canvas = canvas
        reverse_friendship.canvas = canvas
        reverse_friendship.ignored = False
        db.session.add(reverse_friendship)
    db.session.add(friendship)
    db.session.commit()
    if reverse_friendship:
        return ok("accept", "Accepted friend request")
    return ok("request", "Sent friend request")


@app.route("/api/friends/<username>", methods=["DELETE"])
@login_required
@logged_in_limit
def remove_friend(username):
    user = User.by_name(username)
    if not user:
        return error(404, "unknown_user", "No user has that username")
    if user == current_user:
        return error(422, "self", "Self cannot be a friend")
    friendship = Friendship.between(current_user, user)
    reverse_friendship = Friendship.between(user, current_user)
    if friendship and reverse_friendship:
        reverse_friendship.ignored = True
        db.session.add(reverse_friendship)
        db.session.delete(friendship)
        db.session.commit()
        return ok("unfriend", "Unfriended user")
    if friendship and not reverse_friendship:
        db.session.delete(friendship)
        db.session.commit()
        return ok("revoke", "Revoked friend request")
    if not friendship and reverse_friendship:
        if reverse_friendship.ignored:
            return ok("no_op_ignore", "Already ignored friend request")
        reverse_friendship.ignored = True
        db.session.add(reverse_friendship)
        db.session.commit()
        return ok("ignore", "Ignored friend request")
    return ok("no_op_nothing", "Not friends with that user")


@app.route("/api/friends")
@login_required
@logged_in_limit
def get_friends():
    def serialize(users):
        return [u.username for u in users]

    return jsonify(
        friends=serialize(current_user.friends()),
        incoming_requests=serialize(current_user.incoming_friend_requests()),
        outgoing_requests=serialize(current_user.outgoing_friend_requests()),
    )


@app.route("/api/friends_data")
@login_required
@logged_in_limit
def get_friends_data():
    return jsonify(current_user.all_friends_data())


@app.route("/api/friends/<username>/canvas")
@login_required
@logged_in_limit
def get_canvas(username):
    user = User.by_name(username)
    if not user:
        return error(404, "unknown_user", "No user has that username")
    friendship = Friendship.between(current_user, user)
    if not friendship:
        return error(404, "not_friends", "Not friends with that user")
    # if no canvas, check for reciprocating friendship & create if exists
    data = friendship.canvas.data
    if not data:
        return error(404, "no_canvas", "No canvas found")
    return ok("canvas", "Retrieved canvas data", data=b64encode(data))


@app.route("/api/friends/<username>/sync", methods=["POST"])
@login_required
@logged_in_limit
def sync():
    # sync canvas
    pass
