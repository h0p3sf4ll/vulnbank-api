from __future__ import annotations

from flask import Flask, jsonify

from vulnbank.config import Config
from vulnbank.routes import register_blueprints


def create_app(config: Config | None = None) -> Flask:
    app = Flask(__name__)
    cfg = config or Config()
    app.config["SECRET_KEY"] = cfg.secret_key
    app.config["TOKEN_EXPIRY_HOURS"] = cfg.token_expiry_hours
    app.config["DEBUG"] = cfg.debug

    register_blueprints(app)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "app": "VulnBank API"})

    return app
