from __future__ import annotations

from typing import Any


class VulnBankError(Exception):
    pass


class NotFoundError(VulnBankError):
    def __init__(self, resource: str, resource_id: Any) -> None:
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} {resource_id!r} not found")


class InsufficientFundsError(VulnBankError):
    pass
