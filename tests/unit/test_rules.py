from decimal import Decimal

import pytest

from credit_precheck.rules import Route, route 


@pytest.mark.unit
@pytest.mark.parametrize("amount, expected", [
    ("999.99",   Route.REJECTED),
    ("1000.00",  Route.AI_SCORING),
    ("50000.00", Route.AI_SCORING),
    ("50000.01", Route.LOAN_OFFICER),
])
def test_route_by_amount(amount, expected):
    result = route(Decimal(amount), age=30)
    assert result == expected
