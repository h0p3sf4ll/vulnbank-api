from flask import Blueprint, jsonify, request

from vulnbank.auth import get_auth, require_auth
from vulnbank.data import users
from vulnbank.exceptions import NotFoundError

bp = Blueprint("users", __name__, url_prefix="/api/users")


@bp.route("/me", methods=["GET"])
@require_auth
def get_me():
    user = users.get_by_id(get_auth().user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({**user, "profile_url": f"/api/users/{user['id']}"})


@bp.route("/me", methods=["PATCH"])
@require_auth
def update_me():
    data: dict = request.get_json(silent=True) or {}
    try:
        user = users.update(get_auth().user_id, data)
    except NotFoundError:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@bp.route("/<int:user_id>", methods=["GET"])
@require_auth
def get_user(user_id: int):
    user = users.get_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)
