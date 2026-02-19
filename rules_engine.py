# rules_engine.py

HIGH_RISK_COUNTRIES = {"IRAN", "NORTH_KOREA", "SYRIA"}  # use set for faster lookup

AMOUNT_THRESHOLD = 10_000

BASE_SCORE = 10
HIGH_AMOUNT_SCORE = 30
HIGH_RISK_COUNTRY_SCORE = 40

BLOCK_THRESHOLD = 70
REVIEW_THRESHOLD = 40


def evaluate_transaction(tx: dict) -> dict:
    """
    Evaluate a transaction against AML/Fraud rules.

    Expected tx fields:
      - amount: float
      - country: str

    Returns:
      - score: int
      - decision: APPROVE | REVIEW | BLOCK
      - triggered_rules: list[str]
      - rationale: list[str]  # human-readable reasons (audit-friendly)
    """

    score = BASE_SCORE
    triggered = []
    rationale = []

    # -------- Validation / Normalization --------
    try:
        amount = float(tx.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0

    country = str(tx.get("country", "")).upper().strip()

    # -------- Rules --------
    if amount >= AMOUNT_THRESHOLD:
        score += HIGH_AMOUNT_SCORE
        triggered.append("AMOUNT_THRESHOLD")
        rationale.append(f"Amount {amount} >= {AMOUNT_THRESHOLD}")

    if country in HIGH_RISK_COUNTRIES:
        score += HIGH_RISK_COUNTRY_SCORE
        triggered.append("COUNTRY_RISK")
        rationale.append(f"Country {country} is high-risk")

    # -------- Final Decision --------
    if score >= BLOCK_THRESHOLD:
        decision = "BLOCK"
    elif score >= REVIEW_THRESHOLD:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return {
        "score": score,
        "decision": decision,
        "triggered_rules": triggered,
        "rationale": rationale,  # important for compliance / audit trail
    }
