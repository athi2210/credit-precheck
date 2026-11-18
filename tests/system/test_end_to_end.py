import pytest

from credit_precheck.app import build_app
from credit_precheck.bureau import StubBureau
from credit_precheck.model import MockModel
from credit_precheck.rules import Route


@pytest.mark.system
def test_end_to_end_decision_is_explained():
    app = build_app(bureau=StubBureau.realistic(),
                    model=MockModel(score=0.82))

    d = app.assess(amount=15_000, age=34,
                   income=3_200, debt=400)

    assert d.route == Route.AI_SCORING
    assert d.score == 0.82
    assert d.explanation is not None
