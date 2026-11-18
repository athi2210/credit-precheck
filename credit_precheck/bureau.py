from dataclasses import dataclass


class BureauTimeout(Exception):
    """The credit bureau did not answer in time."""


@dataclass(frozen=True)
class CreditReport:
    negative_entries: int


class FakeBureau:
    """In-memory bureau for integration tests. Can simulate a timeout."""

    def __init__(self, simulate_timeout: bool = False, negative_entries: int = 0):
        self.simulate_timeout = simulate_timeout
        self.negative_entries = negative_entries

    def lookup(self, application) -> CreditReport:
        if self.simulate_timeout:
            raise BureauTimeout("credit bureau did not respond")
        return CreditReport(negative_entries=self.negative_entries)


class StubBureau:
    """Returns a canned report for system and acceptance tests."""

    def __init__(self, report: CreditReport):
        self.report = report

    @classmethod
    def realistic(cls) -> "StubBureau":
        return cls(CreditReport(negative_entries=0))

    def lookup(self, application) -> CreditReport:
        return self.report
