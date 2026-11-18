from decimal import Decimal

from credit_precheck.models import Application, Decision
from credit_precheck.service import PrecheckService


class App:
    """Entry point, called the way a user of the system would call it."""

    def __init__(self, service: PrecheckService):
        self.service = service

    def assess(self, amount, age, income, debt) -> Decision:
        application = Application(
            amount=Decimal(str(amount)),
            age=int(age),
            income=Decimal(str(income)),
            debt=Decimal(str(debt)),
        )
        return self.service.assess(application)


def build_app(bureau, model) -> App:
    return App(PrecheckService(bureau, model))
