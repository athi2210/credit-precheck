from credit_precheck.bureau import BureauTimeout
from credit_precheck.models import Application, Decision
from credit_precheck.rules import Route, route


class PrecheckService:
    def __init__(self, bureau, model):
        self.bureau = bureau
        self.model = model

    def assess(self, application: Application) -> Decision:
        r = route(application.amount, application.age)

        if r is Route.INVALID:
            return Decision(r, reason="invalid_application")
        if r is Route.REJECTED:
            return Decision(r, reason="amount_below_minimum")
        if r is Route.LOAN_OFFICER:
            # Large loans are never approved automatically.
            return Decision(r, reason="amount_above_limit")

        try:
            report = self.bureau.lookup(application)
        except BureauTimeout:
            # Never decide alone without bureau data.
            return Decision(Route.LOAN_OFFICER, reason="bureau_unavailable")

        score = self.model.score(application, report)
        return Decision(
            Route.AI_SCORING,
            reason="scored",
            score=score,
            explanation=explain(application, report),
        )


def explain(application: Application, report) -> str:
    ratio = application.debt / application.income
    return (f"Debt-to-income ratio {ratio:.0%}, "
            f"{report.negative_entries} negative bureau entries.")
