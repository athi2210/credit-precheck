from decimal import Decimal
from enum import Enum


class Route(Enum):
    INVALID = "invalid"
    REJECTED = "rejected"
    AI_SCORING = "ai_scoring"
    LOAN_OFFICER = "loan_officer"


def route(amount: Decimal, age: int) -> Route:
    if amount <= 0 or age < 18:
        return Route.INVALID
    if amount < 1000:
        return Route.REJECTED
    if amount <= 50_000:
        return Route.AI_SCORING
    return Route.LOAN_OFFICER
