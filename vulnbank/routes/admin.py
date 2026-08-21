from flask import Blueprint, jsonify

from vulnbank.auth import get_auth, require_admin, require_auth
from vulnbank.data import audit_log, users

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.route("/audit-log", methods=["GET"])
@require_auth
@require_admin
def get_audit_log():
    return jsonify(audit_log.all())


@bp.route("/users", methods=["GET"])
@require_auth
@require_admin
def list_users():
    return jsonify(users.list_all())
