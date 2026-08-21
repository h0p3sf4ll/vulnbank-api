from __future__ import annotations

import datetime

from vulnbank.data import AccountRepository, TransactionRepository
from vulnbank.exceptions import InsufficientFundsError, NotFoundError
from vulnbank.models import Transaction


class TransferService:
    def __init__(
        self,
        accounts: AccountRepository,
        transactions: TransactionRepository,
    ) -> None:
        self._accounts = accounts
        self._transactions = transactions

    def execute(self, from_id: int, to_id: int, amount: float) -> Transaction:
        from_acct = self._accounts.get_by_id(from_id)
        if from_acct is None:
            raise NotFoundError("account", from_id)

        to_acct = self._accounts.get_by_id(to_id)
        if to_acct is None:
            raise NotFoundError("account", to_id)

        if from_acct["balance"] < amount:
            raise InsufficientFundsError

        from_acct["balance"] -= amount
        to_acct["balance"] += amount

        ts = datetime.datetime.now(datetime.timezone.utc)
        txn: Transaction = {
            "id": f"txn-{ts.strftime('%f')[:4]}",
            "account_id": from_id,
            "amount": -amount,
            "description": f"Transfer to account {to_id}",
            "timestamp": ts.isoformat(),
        }
        self._transactions.save(txn)
        return txn
