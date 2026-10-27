from datetime import date, timedelta

import pandas as pd
import streamlit as st

from benefitbridge import EVIDENCE, FEATURES, PRIORITY, check_application
from matching import income_gap, match_score
from messages import TEXT
from proofcheck import check_proof
from schemes import INFO, LAST_CHECKED, LINKS, find_schemes

st.set_page_config(page_title="BenefitBridge", page_icon="🌉")

PROBLEM_CODES = ("small", "dark", "blur", "bad")
SAMPLE_ADDRESS = "12, 3rd Cross, Jayanagar, Bengaluru 560011"
FILE_TYPES = ["jpg", "jpeg", "png", "pdf"]


def detect_issues(app):
    """Problems actually found in the application, in fix-first order."""
    row = pd.Series(app)[FEATURES]
    return [reason for reason in PRIORITY if EVIDENCE[reason](row)]


def build_items(ui, issue_text, found, vals, checks):
    """(do, why, fix) text for every problem: unreadable uploads first."""
    items = []
    for doc, code in checks.items():
        if code in PROBLEM_CODES:
            t = issue_text["unreadable_proof"]
            v = {"doc": ui[doc], "problem": ui["p_" + code]}
            items.append((t["do"].format(**v), t["why"].format(**v),
                          t["fix"].format(**v)))
    for key in found:
        t = issue_text[key]
        items.append((t["do"], t["why"].format(**vals), t["fix"]))
    return items


def checklist_text(ui, items, risk):
    """The checklist as plain text, for the download button."""
    lines = ["BenefitBridge", ui["note"], "",
             f"{ui['risk']}: {risk:.0%}", "", ui["checklist"], ""]
    for i, (do, why, fix) in enumerate(items, 1):
        lines += [f"{i}. {do}", f"   {ui['why']}: {why}",
                  f"   {ui['tip']}: {fix}", ""]
    return "\n".join(lines)


def checker_tab(ui, issue_text):
    today = date.today()
    with st.form("application"):
        c1, c2 = st.columns(2)
        with c1:
            has_id = st.checkbox(ui["l_id"], value=True, key="has_id")
            has_income = st.checkbox(ui["l_income"], value=True, key="has_income")
            has_address = st.checkbox(ui["l_address"], value=True, key="has_address")
            first_time = st.checkbox(ui["l_first"], value=True, key="first_time")
            doc_date = st.date_input(ui["l_doc_date"], value=today - timedelta(days=30),
                                     max_value=today, key="doc_date")
            blank = st.number_input(ui["l_blank"], 0, 20, 0, key="blank")
        with c2:
            name_id = st.text_input(ui["l_name_id"], "Ravi Kumar S", key="name_id")
            name_form = st.text_input(ui["l_name_form"], "Ravi Kumar S", key="name_form")
            addr_proof = st.text_input(ui["l_addr_proof"], SAMPLE_ADDRESS, key="addr_proof")
            addr_form = st.text_input(ui["l_addr_form"], SAMPLE_ADDRESS, key="addr_form")
            inc_form = st.number_input(ui["l_inc_form"], 0, 10_000_000, 20000,
                                       step=1000, key="inc_form")
            inc_proof = st.number_input(ui["l_inc_proof"], 0, 10_000_000, 20000,
                                        step=1000, key="inc_proof")
        st.caption(ui["up_hint"])
        u1, u2, u3 = st.columns(3)
        up_id = u1.file_uploader(ui["l_up_id"], type=FILE_TYPES, key="up_id")
        up_income = u2.file_uploader(ui["l_up_income"], type=FILE_TYPES, key="up_income")
        up_address = u3.file_uploader(ui["l_up_address"], type=FILE_TYPES, key="up_address")
        submitted = st.form_submit_button(ui["check"])

    # Keep the last result so switching language does not erase it.
    # Only the check results are kept, never the uploaded files.
    if submitted:
        checks = {}
        for doc, f in (("doc_id", up_id), ("doc_income", up_income),
                       ("doc_address", up_address)):
            if f is not None:
                checks[doc] = check_proof(f.getvalue(), f.name)
        st.session_state["checks"] = checks
        st.session_state["app"] = {
            "has_id_proof": int(has_id or up_id is not None),
            "has_income_proof": int(has_income or up_income is not None),
            "has_address_proof": int(has_address or up_address is not None),
            "address_proof_age_days": (today - doc_date).days,
            "name_match_score": match_score(name_id, name_form),
            "address_match_score": match_score(addr_proof, addr_form),
            "income_form_vs_proof_gap": income_gap(inc_form, inc_proof),
            "form_fields_blank": blank,
            "first_time_applicant": int(first_time),
        }

    app = st.session_state.get("app")
    if not app:
        return
    checks = st.session_state.get("checks", {})
    out = check_application(app)
    found = detect_issues(app)
    vals = {
        "age": int(app["address_proof_age_days"]),
        "name": f"{int(app['name_match_score'] * 100)}%",
        "addr": f"{int(app['address_match_score'] * 100)}%",
        "gap": f"{app['income_form_vs_proof_gap']:.0%}",
        "blank": int(app["form_fields_blank"]),
    }
    items = build_items(ui, issue_text, found, vals, checks)

    st.metric(ui["risk"], f"{out['rejection_risk']:.0%}")

    if checks:
        st.subheader(ui["up_title"])
        for doc, code in checks.items():
            if code == "ok":
                st.write(f"✔ {ui[doc]}: {ui['up_ok']}")
            elif code == "pdf":
                st.write(f"ℹ {ui[doc]}: {ui['up_pdf']}")
            else:
                st.write(f"✖ {ui[doc]}: {ui['p_' + code]}")
        st.caption(ui["up_note"])

    if not items:
        st.success(ui["ready"])
    else:
        st.warning(ui["fix_first"])
        st.subheader(ui["checklist"])
        for i, (do, why, fix) in enumerate(items, 1):
            st.markdown(f"**{i}. {do}**")
            st.write(f"{ui['why']}: {why}")
            st.write(f"{ui['tip']}: {fix}")
        st.download_button(
            ui["download"],
            data=checklist_text(ui, items, out["rejection_risk"]).encode("utf-8-sig"),
            file_name="benefitbridge_checklist.txt",
            mime="text/plain",
        )


def schemes_tab(ui, lang):
    st.subheader(ui["sf_title"])
    st.caption(ui["sf_intro"])
    show = lambda code: ui["o_" + code]
    with st.form("schemes"):
        c1, c2 = st.columns(2)
        with c1:
            state = st.selectbox(ui["sf_state"], ["KA", "OT"],
                                 format_func=show, key="sf_state")
            age = st.number_input(ui["sf_age"], 0, 110, 30, key="sf_age")
            gender = st.selectbox(ui["sf_gender"], ["W", "M", "O"],
                                  format_func=show, key="sf_gender")
            ration = st.selectbox(ui["sf_ration"], ["NONE", "APL", "BPL", "AAY"],
                                  format_func=show, key="sf_ration")
        with c2:
            woman_head = st.checkbox(ui["sf_head"], key="sf_head")
            tax = st.checkbox(ui["sf_tax"], key="sf_tax")
            govt = st.checkbox(ui["sf_govt"], key="sf_govt")
            power = st.checkbox(ui["sf_power"], key="sf_power")
            yuva = st.checkbox(ui["sf_yuva"], key="sf_yuva")
            farm = st.checkbox(ui["sf_farm"], key="sf_farm")
        go = st.form_submit_button(ui["sf_button"])

    # Only the answers are kept (in this browser session), nothing is stored.
    if go:
        st.session_state["sf"] = {
            "state": state, "age": age, "gender": gender, "ration": ration,
            "woman_head": woman_head, "tax": tax, "govt": govt,
            "power": power, "yuva": yuva, "farm": farm,
        }
    answers = st.session_state.get("sf")
    if not answers:
        return

    st.subheader(ui["sf_results"])
    hits = find_schemes(answers)
    if not hits:
        st.info(ui["sf_none"])
    for sid in hits:
        t = INFO[lang][sid]
        st.markdown(f"**{t['name']}**")
        st.write(f"{ui['sf_gives']}: {t['gives']}")
        st.write(f"{ui['sf_check']}: {t['check']}")
        st.markdown(f"[{ui['sf_link']}]({LINKS[sid]})")
    st.caption(ui["sf_disclaimer"])
    st.caption(ui["sf_checked"].format(date=LAST_CHECKED))


lang = st.radio("Language / भाषा / ಭಾಷೆ", list(TEXT.keys()), horizontal=True)
ui = TEXT[lang]["ui"]
issue_text = TEXT[lang]["issues"]

st.title("BenefitBridge")
st.caption(ui["note"])

tab_check, tab_schemes = st.tabs([ui["tab_check"], ui["tab_schemes"]])
with tab_check:
    checker_tab(ui, issue_text)
with tab_schemes:
    schemes_tab(ui, lang)
