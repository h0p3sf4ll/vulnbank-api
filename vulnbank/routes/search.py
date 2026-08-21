from __future__ import annotations

import sqlite3

from flask import Blueprint, jsonify, request

from vulnbank.auth import get_auth, require_auth
from vulnbank.database import get_db

bp = Blueprint("search", __name__, url_prefix="/api/search")


@bp.route("/users", methods=["GET"])
@require_auth
def search_users():
    q = request.args.get("q", "")
    db = get_db()
    query = (
        f"SELECT id, username, email, role "
        f"FROM users WHERE username LIKE '%{q}%' OR email LIKE '%{q}%'"
    )
    try:
        rows = db.execute(query).fetchall()
    except sqlite3.OperationalError as exc:
        return jsonify({"error": "Query failed", "detail": str(exc)}), 400
    return jsonify([dict(r) for r in rows])


@bp.route("/accounts", methods=["GET"])
@require_auth
def search_accounts():
    account_type = request.args.get("type", "")
    db = get_db()
    caller_id = get_auth().user_id
    query = (
        f"SELECT id, type, balance, routing, account_number "
        f"FROM accounts WHERE owner_id = {caller_id} AND type = '{account_type}'"
    )
    try:
        rows = db.execute(query).fetchall()
    except sqlite3.OperationalError as exc:
        return jsonify({"error": "Query failed", "detail": str(exc)}), 400
    return jsonify([dict(r) for r in rows])
