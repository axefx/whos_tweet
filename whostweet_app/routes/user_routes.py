from flask import Blueprint, jsonify, request, render_template, redirect  # flash
from whostweet_app.models import User, parse_records, db

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users.json")
def list_users():
    users = [
        {"id": 1, "user_handle": "name1"},
        {"id": 2, "user_handle": "name2"},
        {"id": 3, "user_handle": "name3"}
    ]
    user_records = User.query.all()
    print(user_records)
    users = parse_records(user_records)
    return jsonify(users)


@user_routes.route("/users")
def list_users_for_human():
    users = [
        {"id": 1, "user_handle": "name1"},
        {"id": 2, "user_handle": "name2"},
        {"id": 3, "user_handle": "name3"}
    ]
    user_records = User.query.all()
    return render_template("users.html", message="Here's some users", users=user_records)


@user_routes.route("/users/new")
def new_user():
    return render_template("new_user.html")


@user_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA:", dict(request.form))

    new_user = User(
        user_handle=request.form["user_handle"])
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users")
