"""
BenefitBridge - application-readiness prototype
Predicts WHY a benefit application is likely to be rejected/incomplete BEFORE
submission, explains the evidence, and returns a prioritized action checklist.

NOTE: all data here is SIMULATED (synthetic). Label it that way in any demo.

Paste into a Jupyter cell (or run as a script). Needs: numpy, pandas, scikit-learn.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

rng = np.random.default_rng(42)
N = 6000

# ---------------------------------------------------------------- 1. SIMULATED DATA
df = pd.DataFrame({
    "has_id_proof":          rng.choice([0, 1], N, p=[0.04, 0.96]),
    "has_income_proof":      rng.choice([0, 1], N, p=[0.08, 0.92]),
    "has_address_proof":     rng.choice([0, 1], N, p=[0.06, 0.94]),
    # most proofs are recent; a minority are old
    "address_proof_age_days": np.where(rng.random(N) < 0.93,
                                       rng.integers(0, 85, N), rng.integers(91, 365, N)),
    "name_match_score":      np.clip(rng.normal(0.93, 0.12, N), 0, 1),   # ID vs form
    "address_match_score":   np.clip(rng.normal(0.90, 0.15, N), 0, 1),   # proof vs form
    "income_form_vs_proof_gap": np.abs(rng.normal(0, 0.15, N)),          # fraction
    "form_fields_blank":     rng.poisson(0.8, N),
    "first_time_applicant":  rng.choice([0, 1], N, p=[0.55, 0.45]),
})

REASONS = ["ok", "missing_id", "missing_income_proof", "missing_address_proof",
           "expired_address_proof", "name_mismatch", "address_mismatch",
           "income_discrepancy", "incomplete_form"]


def label_row(r):
    # Rule-based ground truth (the simulated "world"), with a little noise
    if r.has_id_proof == 0:                      return "missing_id"
    if r.has_income_proof == 0:                  return "missing_income_proof"
    if r.has_address_proof == 0:                 return "missing_address_proof"
    if r.address_proof_age_days > 90:            return "expired_address_proof"
    if r.name_match_score < 0.80:                return "name_mismatch"
    if r.address_match_score < 0.75:             return "address_mismatch"
    if r.income_form_vs_proof_gap > 0.25:        return "income_discrepancy"
    if r.form_fields_blank >= 3:                 return "incomplete_form"
    return "ok"


df["outcome"] = df.apply(label_row, axis=1)
flip = rng.random(N) < 0.03                       # 3% label noise
df.loc[flip, "outcome"] = rng.choice(REASONS, flip.sum())

FEATURES = [c for c in df.columns if c != "outcome"]
X_tr, X_te, y_tr, y_te = train_test_split(
    df[FEATURES], df["outcome"], test_size=0.25, random_state=1, stratify=df["outcome"])

# ---------------------------------------------------------------- 2. MODEL
model = RandomForestClassifier(n_estimators=300, random_state=1, n_jobs=-1)
model.fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te), zero_division=0))

# ---------------------------------------------------------------- 3. ACTIONS + EXPLANATION
ACTIONS = {
    "missing_id":            "Upload a government ID (Aadhaar / passport / voter ID).",
    "missing_income_proof":  "Upload income proof (salary slip or income certificate).",
    "missing_address_proof": "Upload address proof (utility bill, rent agreement).",
    "expired_address_proof": "Replace address proof with one dated within the last 90 days.",
    "name_mismatch":         "Make the name on the form match your ID exactly (spelling, initials).",
    "address_mismatch":      "Make the address on the form match your address proof.",
    "income_discrepancy":    "Correct the income on the form or attach a proof that supports it.",
    "incomplete_form":       "Fill in all blank form fields before submitting.",
}
EVIDENCE = {
    "missing_id":            lambda r: "No ID proof attached." if r.has_id_proof == 0 else None,
    "missing_income_proof":  lambda r: "No income proof attached." if r.has_income_proof == 0 else None,
    "missing_address_proof": lambda r: "No address proof attached." if r.has_address_proof == 0 else None,
    "expired_address_proof": lambda r: (f"Address proof is {int(r.address_proof_age_days)} days old (limit 90)."
                                        if r.address_proof_age_days > 90 else None),
    "name_mismatch":         lambda r: (f"Name match score {r.name_match_score:.2f} (needs 0.80+)."
                                        if r.name_match_score < 0.80 else None),
    "address_mismatch":      lambda r: (f"Address match score {r.address_match_score:.2f} (needs 0.75+)."
                                        if r.address_match_score < 0.75 else None),
    "income_discrepancy":    lambda r: (f"Form income differs from proof by {r.income_form_vs_proof_gap:.0%} (limit 25%)."
                                        if r.income_form_vs_proof_gap > 0.25 else None),
    "incomplete_form":       lambda r: (f"{int(r.form_fields_blank)} form fields are blank."
                                        if r.form_fields_blank >= 3 else None),
}
# Fix-first priority: cheapest blockers to unblock a submission come first
PRIORITY = ["missing_id", "missing_income_proof", "missing_address_proof",
            "expired_address_proof", "name_mismatch", "address_mismatch",
            "income_discrepancy", "incomplete_form"]


def check_application(app: dict) -> dict:
    """app: dict with the FEATURES keys. Returns risk, predicted reason, evidence, checklist."""
    row = pd.Series(app)[FEATURES]
    proba = model.predict_proba(row.to_frame().T.astype(float))[0]
    classes = list(model.classes_)
    p = dict(zip(classes, proba))
    risk = 1.0 - p.get("ok", 0.0)
    top = max((c for c in classes if c != "ok"), key=lambda c: p[c])

    # Evidence-backed issues (what the data actually shows), ranked by priority
    issues = []
    for reason in PRIORITY:
        ev = EVIDENCE[reason](row)
        if ev:
            issues.append((reason, ev, p.get(reason, 0.0)))
    checklist = [f"{i+1}. {ACTIONS[r]}  (why: {ev})" for i, (r, ev, _) in enumerate(issues)]

    return {
        "rejection_risk": round(risk, 2),
        "most_likely_reason": top,
        "model_confidence": round(p[top], 2),
        "evidence": [ev for _, ev, _ in issues],
        "action_checklist": checklist or ["No problems found. Application looks ready to submit."],
    }


# ---------------------------------------------------------------- 4. DEMO
if __name__ == "__main__":
    demo = {"has_id_proof": 1, "has_income_proof": 1, "has_address_proof": 1,
            "address_proof_age_days": 140, "name_match_score": 0.72,
            "address_match_score": 0.92, "income_form_vs_proof_gap": 0.05,
            "form_fields_blank": 1, "first_time_applicant": 1}
    out = check_application(demo)
    print("\nRejection risk:", out["rejection_risk"],
          "| Likely reason:", out["most_likely_reason"], f"({out['model_confidence']})")
    print("Action checklist:")
    for line in out["action_checklist"]:
        print("  ", line)

    # Measurable result on SIMULATED data: how often does the checker flag
    # applications that would have failed?
    pred = model.predict(X_te)
    would_fail = y_te != "ok"
    flagged = pred != "ok"
    print(f"\nSimulated test set: {would_fail.mean():.0%} of applications would fail;")
    print(f"checker flags {(flagged & would_fail).sum()/would_fail.sum():.0%} of them before submission "
          f"(false alarms: {(flagged & ~would_fail).sum()/ (~would_fail).sum():.0%}).")
