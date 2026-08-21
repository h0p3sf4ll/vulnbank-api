from flask import Flask

from vulnbank.routes.accounts import bp as accounts_bp
from vulnbank.routes.admin import bp as admin_bp
from vulnbank.routes.auth import bp as auth_bp
from vulnbank.routes.messages import bp as messages_bp
from vulnbank.routes.transfers import bp as transfers_bp
from vulnbank.routes.users import bp as users_bp


def register_blueprints(app: Flask) -> None:
    for bp in (auth_bp, users_bp, accounts_bp, transfers_bp, messages_bp, admin_bp):
        app.register_blueprint(bp)
