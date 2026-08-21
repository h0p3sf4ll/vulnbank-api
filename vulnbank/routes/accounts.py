from flask import Blueprint, jsonify

from vulnbank.auth import get_auth, require_auth
from vulnbank.data import accounts, transactions

bp = Blueprint("accounts", __name__, url_prefix="/api")


@bp.route("/accounts", methods=["GET"])
@require_auth
def list_accounts():
    owned = accounts.list_by_owner(get_auth().user_id)
    safe = [{**a, "account_number": "****" + a["account_number"][-4:]} for a in owned]
    return jsonify(safe)


@bp.route("/accounts/<int:account_id>", methods=["GET"])
@require_auth
def get_account(account_id: int):
    account = accounts.get_by_id(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account)


@bp.route("/accounts/<int:account_id>/transactions", methods=["GET"])
@require_auth
def list_transactions(account_id: int):
    account = accounts.get_by_id(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(transactions.list_by_account(account_id))


@bp.route("/transactions/<txn_id>", methods=["GET"])
@require_auth
def get_transaction(txn_id: str):
    txn = transactions.get_by_id(txn_id)
    if txn is None:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify(txn)
