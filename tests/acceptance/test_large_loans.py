import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from credit_precheck.app import build_app
from credit_precheck.bureau import StubBureau
from credit_precheck.model import MockModel
from credit_precheck.rules import Route

pytestmark = pytest.mark.acceptance

scenarios("large_loans.feature")


@given(parsers.parse("an applicant aged {age:d} with good credit"),
       target_fixture="applicant")
def applicant(age):
    return {"age": age, "income": 4_000, "debt": 300}


@when(parsers.parse("a loan of {amount} EUR is requested"),
      target_fixture="decision")
def request_loan(applicant, amount):
    app = build_app(bureau=StubBureau.realistic(),
                    model=MockModel(score=0.95))
    return app.assess(amount=amount.replace(",", ""), **applicant)


@then("the request goes to a loan officer")
def goes_to_loan_officer(decision):
    assert decision.route == Route.LOAN_OFFICER


@then("no automatic approval is given")
def no_automatic_approval(decision):
    assert decision.route != Route.AI_SCORING
    assert decision.score is None
