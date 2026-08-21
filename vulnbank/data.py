from __future__ import annotations

from typing import Any

from vulnbank.exceptions import NotFoundError
from vulnbank.models import Account, AuditEntry, Message, Transaction, User


class UserRepository:
    PROTECTED_FIELDS: frozenset[str] = frozenset({"id", "username", "ssn"})

    def __init__(self, store: dict[int, User], passwords: dict[str, str]) -> None:
        self._store = store
        self._passwords = passwords

    def get_by_id(self, user_id: int) -> User | None:
        return self._store.get(user_id)

    def get_by_username(self, username: str) -> User | None:
        return next((u for u in self._store.values() if u["username"] == username), None)

    def verify_password(self, username: str, password: str) -> bool:
        return self._passwords.get(username) == password

    def update(self, user_id: int, fields: dict[str, Any]) -> User:
        user = self._store.get(user_id)
        if user is None:
            raise NotFoundError("user", user_id)
        for key, value in fields.items():
            if key not in self.PROTECTED_FIELDS:
                user[key] = value  # type: ignore[literal-required]
        return user

    def list_all(self) -> list[User]:
        return list(self._store.values())


class AccountRepository:
    def __init__(self, store: dict[int, Account]) -> None:
        self._store = store

    def get_by_id(self, account_id: int) -> Account | None:
        return self._store.get(account_id)

    def list_by_owner(self, owner_id: int) -> list[Account]:
        return [a for a in self._store.values() if a["owner_id"] == owner_id]


class TransactionRepository:
    def __init__(self, store: dict[str, Transaction]) -> None:
        self._store = store

    def get_by_id(self, txn_id: str) -> Transaction | None:
        return self._store.get(txn_id)

    def list_by_account(self, account_id: int) -> list[Transaction]:
        return [t for t in self._store.values() if t["account_id"] == account_id]

    def save(self, txn: Transaction) -> None:
        self._store[txn["id"]] = txn


class MessageRepository:
    def __init__(self, store: dict[str, Message]) -> None:
        self._store = store

    def get_by_id(self, message_id: str) -> Message | None:
        return self._store.get(message_id)

    def list_by_recipient(self, recipient_id: int) -> list[Message]:
        return [m for m in self._store.values() if m["recipient_id"] == recipient_id]


class AuditRepository:
    def __init__(self, log: list[AuditEntry]) -> None:
        self._log = log

    def all(self) -> list[AuditEntry]:
        return self._log


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

_USERS: dict[int, User] = {
    1: {"id": 1, "username": "alice",   "email": "alice@vulnbank.com",   "role": "user",  "ssn": "123-45-6789", "balance": 5000.00},
    2: {"id": 2, "username": "bob",     "email": "bob@vulnbank.com",     "role": "user",  "ssn": "987-65-4321", "balance": 12500.00},
    3: {"id": 3, "username": "charlie", "email": "charlie@vulnbank.com", "role": "user",  "ssn": "555-44-3333", "balance": 750.00},
    4: {"id": 4, "username": "admin",   "email": "admin@vulnbank.com",   "role": "admin", "ssn": "000-00-0001", "balance": 0.00},
}

_PASSWORDS: dict[str, str] = {
    "alice":   "password123",
    "bob":     "hunter2",
    "charlie": "ilovecats",
    "admin":   "Adm1n$ecure!",
}

_ACCOUNTS: dict[int, Account] = {
    101: {"id": 101, "owner_id": 1, "type": "checking", "balance": 5000.00,  "routing": "021000021", "account_number": "4111111111110001"},
    102: {"id": 102, "owner_id": 1, "type": "savings",  "balance": 22000.00, "routing": "021000021", "account_number": "4111111111110002"},
    103: {"id": 103, "owner_id": 2, "type": "checking", "balance": 12500.00, "routing": "021000021", "account_number": "4111111111110003"},
    104: {"id": 104, "owner_id": 3, "type": "checking", "balance": 750.00,   "routing": "021000021", "account_number": "4111111111110004"},
}

_TRANSACTIONS: dict[str, Transaction] = {
    "txn-a3f1": {"id": "txn-a3f1", "account_id": 101, "amount": -200.00,  "description": "Coffee Shop",                              "timestamp": "2024-01-15T09:23:00Z"},
    "txn-b8c2": {"id": "txn-b8c2", "account_id": 101, "amount": 3000.00,  "description": "Payroll deposit",                          "timestamp": "2024-01-14T00:01:00Z"},
    "txn-d4e9": {"id": "txn-d4e9", "account_id": 103, "amount": -5500.00, "description": "Rent payment",                             "timestamp": "2024-01-13T11:00:00Z"},
    "txn-f7a0": {"id": "txn-f7a0", "account_id": 104, "amount": -49.99,   "description": "Streaming subscription",                   "timestamp": "2024-01-12T18:45:00Z"},
    "txn-c1b5": {"id": "txn-c1b5", "account_id": 102, "amount": 22000.00, "description": "Wire transfer — CONFIDENTIAL SETTLEMENT",  "timestamp": "2024-01-10T14:00:00Z"},
}

_MESSAGES: dict[str, Message] = {
    "msg-4429": {"id": "msg-4429", "recipient_id": 1, "sender": "VulnBank Security", "subject": "Your 2FA backup codes",               "body": "Your backup codes are: 83621, 94715, 20384, 11029, 76543"},
    "msg-7731": {"id": "msg-7731", "recipient_id": 2, "sender": "VulnBank Support",  "subject": "Account review complete",             "body": "Hi Bob, your account review is complete. No issues found."},
    "msg-0815": {"id": "msg-0815", "recipient_id": 1, "sender": "VulnBank Fraud",    "subject": "Suspicious activity alert",           "body": "We flagged a login from IP 198.51.100.42. If this wasn't you, call 1-800-555-0199."},
    "msg-3356": {"id": "msg-3356", "recipient_id": 3, "sender": "Loan Department",   "subject": "Loan application #LN-9981 APPROVED",  "body": "Congratulations Charlie! Your $25,000 personal loan has been approved."},
}

_AUDIT_LOG: list[AuditEntry] = [
    {"event": "login",          "user_id": 1, "ip": "203.0.113.5",   "timestamp": "2024-01-15T09:00:00Z"},
    {"event": "transfer",       "user_id": 2, "ip": "198.51.100.42", "timestamp": "2024-01-14T22:31:00Z", "details": {"from_account": 103, "to_account": 101, "amount": 9500.00}},
    {"event": "login",          "user_id": 3, "ip": "192.0.2.88",    "timestamp": "2024-01-13T08:15:00Z"},
    {"event": "profile_update", "user_id": 2, "ip": "198.51.100.42", "timestamp": "2024-01-14T20:11:00Z", "details": {"fields_modified": ["role"]}},
    {"event": "admin_request",  "user_id": 2, "ip": "198.51.100.42", "timestamp": "2024-01-14T20:15:00Z", "details": {"path": "/api/admin/users", "status": 200}},
]

# Module-level singletons — one shared instance per process
users = UserRepository(_USERS, _PASSWORDS)
accounts = AccountRepository(_ACCOUNTS)
transactions = TransactionRepository(_TRANSACTIONS)
messages = MessageRepository(_MESSAGES)
audit_log = AuditRepository(_AUDIT_LOG)
