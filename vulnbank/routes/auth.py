from flask import Blueprint, jsonify, request

from vulnbank.auth import create_token
from vulnbank.data import users

bp = Blueprint("auth", __name__)


@bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username: str = data.get("username", "")
    password: str = data.get("password", "")

    if not users.verify_password(username, password):
        return jsonify({"error": "Invalid credentials"}), 401

    user = users.get_by_username(username)
    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(user["id"], user["role"])
    return jsonify({"token": token, "user_id": user["id"]})
