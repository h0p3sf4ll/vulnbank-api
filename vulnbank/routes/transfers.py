from flask import Blueprint, jsonify, request

from vulnbank.auth import require_auth
from vulnbank.data import accounts, transactions
from vulnbank.exceptions import InsufficientFundsError, NotFoundError
from vulnbank.services import TransferService

bp = Blueprint("transfers", __name__, url_prefix="/api")

_transfer_service = TransferService(accounts, transactions)


@bp.route("/transfers", methods=["POST"])
@require_auth
def create_transfer():
    data = request.get_json(silent=True) or {}
    from_id = data.get("from_account")
    to_id = data.get("to_account")
    amount = data.get("amount")

    if from_id is None or to_id is None or amount is None:
        return jsonify({"error": "from_account, to_account, and amount are required"}), 400

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    try:
        txn = _transfer_service.execute(int(from_id), int(to_id), amount)
    except NotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except InsufficientFundsError:
        return jsonify({"error": "Insufficient funds"}), 422

    src = accounts.get_by_id(int(from_id))
    return jsonify({
        "status": "ok",
        "transaction_id": txn["id"],
        "new_balance": src["balance"] if src else None,
    })
