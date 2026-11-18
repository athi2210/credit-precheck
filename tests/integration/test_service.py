from decimal import Decimal

import pytest

from credit_precheck.bureau import FakeBureau
from credit_precheck.model import MockModel
from credit_precheck.models import Application
from credit_precheck.rules import Route
from credit_precheck.service import PrecheckService


def applicant(amount="20000", age=30, income="3000", debt="500"):
    return Application(Decimal(amount), age, Decimal(income), Decimal(debt))


@pytest.mark.integration
def test_bureau_timeout_falls_back_to_officer():
    bureau = FakeBureau(simulate_timeout=True)
    model = MockModel(score=0.7)
    service = PrecheckService(bureau, model)

    d = service.assess(applicant(amount="20000"))

    assert d.route == Route.LOAN_OFFICER
    assert d.reason == "bureau_unavailable"
