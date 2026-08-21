from __future__ import annotations

import datetime
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, TypeVar

import jwt
from flask import current_app, g, jsonify, request

F = TypeVar("F", bound=Callable[..., Any])

_AUTH_CTX_KEY = "_auth"


@dataclass(frozen=True)
class AuthContext:
    user_id: int
    role: str


def get_auth() -> AuthContext:
    ctx: AuthContext | None = getattr(g, _AUTH_CTX_KEY, None)
    if ctx is None:
        raise RuntimeError("No auth context — require_auth decorator not applied")
    return ctx


def create_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=current_app.config["TOKEN_EXPIRY_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def require_auth(f: F) -> F:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header[7:]
        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            setattr(g, _AUTH_CTX_KEY, AuthContext(user_id=payload["user_id"], role=payload["role"]))
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated  # type: ignore[return-value]


def require_admin(f: F) -> F:
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if get_auth().role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)

    return decorated  # type: ignore[return-value]
