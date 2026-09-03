from __future__ import annotations

import json
import urllib.request
from urllib.error import URLError

from flask import Blueprint, jsonify, request

from vulnbank.auth import require_auth
from vulnbank.data import transactions

bp = Blueprint("receipts", __name__, url_prefix="/api/transfers")


@bp.route("/<txn_id>/receipt", methods=["POST"])
@require_auth
def send_receipt(txn_id: str):
    """Deliver a transaction receipt to a caller-supplied webhook URL."""
    data = request.get_json(silent=True) or {}
    webhook_url = data.get("webhook_url")
    if not webhook_url:
        return jsonify({"error": "webhook_url is required"}), 400

    txn = transactions.get_by_id(txn_id)
    if txn is None:
        return jsonify({"error": "Transaction not found"}), 404

    receipt = {
        "transaction_id": txn["id"],
        "amount": txn["amount"],
        "description": txn["description"],
        "timestamp": txn["timestamp"],
    }

    try:
        payload = json.dumps(receipt).encode()
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=5)
    except URLError as exc:
        return jsonify({"error": "Webhook delivery failed", "detail": str(exc)}), 502

    return jsonify({"status": "delivered", "url": webhook_url})
