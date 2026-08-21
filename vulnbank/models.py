from __future__ import annotations

from typing import Any, TypedDict


class User(TypedDict):
    id: int
    username: str
    email: str
    role: str
    ssn: str
    balance: float


class Account(TypedDict):
    id: int
    owner_id: int
    type: str
    balance: float
    routing: str
    account_number: str


class Transaction(TypedDict):
    id: str
    account_id: int
    amount: float
    description: str
    timestamp: str


class Message(TypedDict):
    id: str
    recipient_id: int
    sender: str
    subject: str
    body: str


class AuditEntry(TypedDict, total=False):
    event: str
    user_id: int
    ip: str
    timestamp: str
    details: dict[str, Any]
