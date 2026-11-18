class MockModel:
    """Stands in for the ML model: always returns the same score."""

    def __init__(self, score: float):
        self._score = score

    def score(self, application, report) -> float:
        return self._score
