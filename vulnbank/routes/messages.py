from flask import Blueprint, jsonify

from vulnbank.auth import get_auth, require_auth
from vulnbank.data import messages

bp = Blueprint("messages", __name__, url_prefix="/api/messages")


@bp.route("", methods=["GET"])
@require_auth
def list_messages():
    inbox = messages.list_by_recipient(get_auth().user_id)
    return jsonify([{"id": m["id"], "sender": m["sender"], "subject": m["subject"]} for m in inbox])


@bp.route("/<message_id>", methods=["GET"])
@require_auth
def get_message(message_id: str):
    msg = messages.get_by_id(message_id)
    if msg is None:
        return jsonify({"error": "Message not found"}), 404
    return jsonify(msg)
