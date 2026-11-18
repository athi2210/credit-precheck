from dataclasses import dataclass
from decimal import Decimal

from credit_precheck.rules import Route


@dataclass(frozen=True)
class Application:
    amount: Decimal
    age: int
    income: Decimal  # monthly net income
    debt: Decimal    # monthly debt payments


@dataclass(frozen=True)
class Decision:
    route: Route
    reason: str
    score: float | None = None
    explanation: str | None = None
