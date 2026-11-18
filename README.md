# credit-precheck

> **This is a demo project.** It was built for a university talk on software
> testing levels. Its only purpose is to show unit, integration and system
> tests on a small, understandable example. It is **not** a real
> credit-check system: there is no real credit bureau, no real ML model, no
> database and no user interface, and the business rules are simplified.

## The idea

A bank pre-checks consumer loan applications before anyone looks at them.
Each application passes through these steps:

```
Loan application -> Rule engine -> Credit bureau -> ML scoring (mock) -> Explanation -> Decision
```

The result is a **routing decision**: who or what handles the application next,
and why. It is not a final "approved" or "declined".

## Architecture

```
            build_app(bureau, model)          app.py      entry point, raw input -> Application
                       │
                       ▼
               PrecheckService                service.py  orchestrates the steps below
              ┌────────┼─────────────┐
              ▼        ▼             ▼
          route()    bureau        model
         rules.py   bureau.py     model.py
       (amount,    (credit       (score from
         age)       history)      application + bureau data)
                       │
                       ▼
                   Decision                   models.py   route, reason, score, explanation
```

| Component | File | Responsibility |
|-----------|------|----------------|
| Rule engine | `credit_precheck/rules.py` | `route(amount, age)` sorts an application into one of four routes, using only data from the application itself. |
| Credit bureau | `credit_precheck/bureau.py` | Supplies external credit history (here only the number of negative entries). `FakeBureau` can simulate a timeout; `StubBureau.realistic()` always returns a healthy report. |
| ML model | `credit_precheck/model.py` | `MockModel(score)` stands in for a trained model and always returns the same score. |
| Service | `credit_precheck/service.py` | `PrecheckService` connects the parts and builds a short explanation of the score. |
| Entry point | `credit_precheck/app.py` | `build_app(...)` wires everything together; `assess(amount, age, income, debt)` accepts plain numbers. |
| Data | `credit_precheck/models.py` | `Application` (input) and `Decision` (output) dataclasses. Money is always `Decimal`. |

The service receives the bureau and the model from outside (dependency
injection). That is what lets each test level swap in a fake or a stub.

## How it works

1. **Rules first.** `route()` checks amount and age:

   | Condition | Route |
   |-----------|-------|
   | amount <= 0 or age < 18 | `INVALID` |
   | amount < 1,000 | `REJECTED` |
   | 1,000 <= amount <= 50,000 | `AI_SCORING` |
   | amount > 50,000 | `LOAN_OFFICER` (never approved automatically) |

   `INVALID`, `REJECTED` and `LOAN_OFFICER` stop here.
2. **Credit bureau.** For `AI_SCORING`, the service asks the bureau for the
   applicant's credit history. If the bureau times out, the application goes to
   `LOAN_OFFICER` with reason `bureau_unavailable`: the system never decides
   alone without bureau data.
3. **Scoring and explanation.** The model returns a score, and the service adds
   an explanation of the factors behind it, e.g.
   `Debt-to-income ratio 12%, 0 negative bureau entries.`

### Simplifications

- A score is returned, but there is no threshold that turns it into "approved".
- Applications above 50,000 € skip the bureau and the model, so the loan
  officer gets no score or explanation.

## Test levels

There is one test per level. Each level asks a different question:

| Level | Test | Question | Bureau / model |
|-------|------|----------|----------------|
| Unit | `tests/unit/test_rules.py` | Are the amount boundaries of `route()` correct? (999.99 / 1000.00 / 50000.00 / 50000.01) | none |
| Integration | `tests/integration/test_service.py` | Does the service fall back to a loan officer when the bureau times out? | `FakeBureau(simulate_timeout=True)` |
| System | `tests/system/test_end_to_end.py` | Does the whole application, called from outside, return a scored and explained decision? | `StubBureau.realistic()` |
## Setup

Requires Python 3.11+.

```
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Running the demo

```
python demo.py
```

Runs five sample applications (normal, large, too small, underage, bureau
unavailable) through the pre-check and prints each decision.

## Running the tests

| Level | Command |
|-------|---------|
| Unit        | `pytest -m unit -v` |
| Integration | `pytest -m integration -v` |
| System      | `pytest -m system -v` || All         | `pytest -v` |

## About this project

This project was built with the help of an AI coding assistant.
