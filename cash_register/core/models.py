"""
models.py — Pure data models. Zero UI dependency.
All business logic that touches data lives here.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Transaction:
    date: str
    name: str
    cr: float = 0.0
    dr: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Transaction":
        return cls(
            date=d.get("date", ""),
            name=d.get("name", ""),
            cr=float(d.get("cr") or 0.0),
            dr=float(d.get("dr") or 0.0),
        )


@dataclass
class LedgerState:
    opening_cash: Optional[float] = None
    current_date: Optional[str]   = None
    rows: List[Transaction]        = field(default_factory=list)

    # ── computed properties ───────────────────────────────────────────────────

    @property
    def is_initialised(self) -> bool:
        return self.opening_cash is not None

    @property
    def total_cr(self) -> float:
        return sum(r.cr for r in self.rows)

    @property
    def total_dr(self) -> float:
        return sum(r.dr for r in self.rows)

    @property
    def cash_in_hand(self) -> float:
        return (self.opening_cash or 0.0) + self.total_cr - self.total_dr

    def running_balance_at(self, index: int) -> float:
        """Cash in hand after applying rows[0..index] (inclusive)."""
        balance = self.opening_cash or 0.0
        for i, row in enumerate(self.rows):
            balance += row.cr - row.dr
            if i == index:
                return balance
        return balance

    # ── mutations ─────────────────────────────────────────────────────────────

    def add_row(self, tx: Transaction) -> None:
        self.rows.append(tx)

    def update_row(self, index: int, tx: Transaction) -> None:
        self.rows[index] = tx

    def delete_row(self, index: int) -> None:
        del self.rows[index]

    def roll_to_new_date(self, new_date: str) -> None:
        """Archive current day: carry closing balance forward, clear rows."""
        closing = self.cash_in_hand
        self.opening_cash = closing
        self.current_date = new_date
        self.rows = []

    # ── serialisation ─────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "opening_cash": self.opening_cash,
            "current_date": self.current_date,
            "rows": [r.to_dict() for r in self.rows],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "LedgerState":
        return cls(
            opening_cash=d.get("opening_cash"),
            current_date=d.get("current_date"),
            rows=[Transaction.from_dict(r) for r in d.get("rows", [])],
        )
