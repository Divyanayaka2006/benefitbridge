import streamlit as st
from benefitbridge import check_application

st.set_page_config(page_title="BenefitBridge", page_icon="🌉")
st.title("BenefitBridge")
st.caption("Application-readiness checker. Built on simulated data; "
           "not an eligibility decision.")

with st.form("application"):
    c1, c2 = st.columns(2)
    with c1:
        has_id = st.checkbox("ID proof attached", value=True)
        has_income = st.checkbox("Income proof attached", value=True)
        has_address = st.checkbox("Address proof attached", value=True)
        first_time = st.checkbox("First-time applicant", value=True)
        age_days = st.number_input("Address proof age (days)", 0, 730, 30)
    with c2:
        name_score = st.slider("Name match score (ID vs form)", 0.0, 1.0, 0.95)
        addr_score = st.slider("Address match score (proof vs form)", 0.0, 1.0, 0.95)
        income_gap = st.slider("Income gap, form vs proof", 0.0, 1.0, 0.05)
        blank = st.number_input("Blank form fields", 0, 20, 0)
    submitted = st.form_submit_button("Check my application")

if submitted:
    app = {
        "has_id_proof": int(has_id),
        "has_income_proof": int(has_income),
        "has_address_proof": int(has_address),
        "address_proof_age_days": age_days,
        "name_match_score": name_score,
        "address_match_score": addr_score,
        "income_form_vs_proof_gap": income_gap,
        "form_fields_blank": blank,
        "first_time_applicant": int(first_time),
    }
    out = check_application(app)
    st.metric("Rejection risk", f"{out['rejection_risk']:.0%}")
    if out["rejection_risk"] >= 0.5:
        st.warning(f"Most likely reason: {out['most_likely_reason']}")
    else:
        st.success("Looks ready to submit.")
    st.subheader("Action checklist")
    for line in out["action_checklist"]:
        st.write(line)