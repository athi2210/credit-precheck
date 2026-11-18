"""Runs a few sample loan applications through the pre-check.

Usage: python demo.py
"""
from credit_precheck.app import build_app
from credit_precheck.bureau import FakeBureau, StubBureau
from credit_precheck.model import MockModel

app = build_app(bureau=StubBureau.realistic(), model=MockModel(score=0.82))
offline_app = build_app(bureau=FakeBureau(simulate_timeout=True),
                        model=MockModel(score=0.7))

cases = [
    ("Normal loan",         app,         dict(amount=15_000, age=34, income=3_200, debt=400)),
    ("Large loan",          app,         dict(amount=60_000, age=40, income=4_000, debt=300)),
    ("Too small",           app,         dict(amount=500,    age=25, income=2_000, debt=0)),
    ("Underage applicant",  app,         dict(amount=5_000,  age=17, income=800,   debt=0)),
    ("Bureau unavailable",  offline_app, dict(amount=20_000, age=30, income=3_000, debt=500)),
]

for title, a, application in cases:
    d = a.assess(**application)
    print(f"{title}  ({application['amount']:,} EUR, age {application['age']})")
    print(f"  route:       {d.route.value}")
    print(f"  reason:      {d.reason}")
    if d.score is not None:
        print(f"  score:       {d.score}")
        print(f"  explanation: {d.explanation}")
    print()
