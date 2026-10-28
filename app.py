from datetime import date, timedelta

import pandas as pd
import streamlit as st

from benefitbridge import EVIDENCE, FEATURES, PRIORITY, check_application
from explain import (CHECKABLE, DOC_FOOTER, DOC_LABEL, DOC_TEXT, LABELS,
                     LINK_FALLBACK, MATCH_TEXT, NO_LINK, SUMMARY, VERIFY_TEXT, build_summary,
                     documents, explain)
from matching import income_gap, match_score
from steps import QUESTIONS, STEP_TEXT
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


def all_at_once(ui):
    """The original form: every question on one screen."""
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
    return st.session_state.get("sf")


def _pick(key, value, nxt):
    st.session_state["step_ans"][key] = value
    st.session_state["step_i"] = nxt


def _pick_age(nxt):
    _pick("age", st.session_state["step_age"], nxt)


def _go(n):
    st.session_state["step_i"] = n


def _restart():
    st.session_state["step_ans"] = {}
    st.session_state["step_i"] = 0


def one_at_a_time(ui, lang):
    """One big question per screen. Returns the answers when all are done."""
    T = STEP_TEXT[lang]
    total = len(QUESTIONS)
    st.session_state.setdefault("step_ans", {})
    i = st.session_state.setdefault("step_i", 0)

    if i >= total:
        st.button(T["back"], key="done_back", on_click=_go, args=(total - 1,))
        st.button(T["restart"], key="done_restart", on_click=_restart)
        return dict(st.session_state["step_ans"])

    q = QUESTIONS[i]
    st.progress(i / total)
    st.caption(T["progress"].format(n=i + 1, total=total))
    st.subheader(q["icon"] + "  " + (ui[q["ui"]] if "ui" in q else T[q["text"]]))

    if q["kind"] == "choice":
        for opt in q["options"]:
            st.button(ui["o_" + opt], key=f"a{i}_{opt}", on_click=_pick,
                      args=(q["key"], opt, i + 1), use_container_width=True)
    elif q["kind"] == "yesno":
        st.button(T["yes"], key=f"a{i}_yes", on_click=_pick,
                  args=(q["key"], True, i + 1), use_container_width=True)
        st.button(T["no"], key=f"a{i}_no", on_click=_pick,
                  args=(q["key"], False, i + 1), use_container_width=True)
    else:  # number (age)
        st.number_input(T["q_age"], 0, 110,
                        st.session_state["step_ans"].get("age", 30),
                        key="step_age", label_visibility="collapsed")
        st.button(T["next"], key=f"a{i}_next", on_click=_pick_age,
                  args=(i + 1,), use_container_width=True)
    if i > 0:
        st.button(T["back"], key=f"back{i}", on_click=_go, args=(i - 1,))
    return None


def show_results(ui, lang, answers):
    st.subheader(ui["sf_results"])
    hits = find_schemes(answers)
    if not hits:
        st.info(ui["sf_none"])
    have = set()  # (scheme, document) pairs the person ticked
    for sid in hits:
        t = INFO[lang][sid]
        st.markdown(f"**{t['name']}**")
        st.write(f"{ui['sf_gives']}: {t['gives']}")
        st.write(f"{ui['sf_check']}: {t['check']}")
        matched, verify = explain(sid, answers)
        with st.expander(LABELS[lang]["why"] + " / " + LABELS[lang]["verify"]):
            st.markdown(f"**{LABELS[lang]['why']}**")
            for key in matched:
                st.write("✔ " + MATCH_TEXT[lang][key])
            st.markdown(f"**{LABELS[lang]['verify']}**")
            for key in verify:
                st.write("➤ " + VERIFY_TEXT[lang][key])
            st.markdown(f"**{DOC_LABEL[lang]}**")
            st.caption(SUMMARY[lang]["tick"])
            for key in documents(sid, matched):
                if key in CHECKABLE:
                    if st.checkbox("📄 " + DOC_TEXT[lang][key],
                                   key=f"have_{sid}_{key}"):
                        have.add((sid, key))
                else:
                    st.write("📄 " + DOC_TEXT[lang][key])
            st.caption(DOC_FOOTER[lang])
        if LINKS.get(sid):
            st.markdown(f"[{ui['sf_link']}]({LINKS[sid]})")
            st.caption(LINK_FALLBACK[lang])
        else:
            st.caption(NO_LINK[lang])
    if hits:
        st.divider()
        st.subheader(SUMMARY[lang]["title"])
        st.download_button(
            SUMMARY[lang]["download"],
            data=build_summary(lang, ui, hits, answers, have, INFO, LINKS,
                               LAST_CHECKED).encode("utf-8-sig"),
            file_name="benefitbridge_summary.txt",
            mime="text/plain",
        )
        st.caption(SUMMARY[lang]["check_tab"].format(tab=ui["tab_check"]))
    st.caption(ui["sf_disclaimer"])
    st.caption(ui["sf_checked"].format(date=LAST_CHECKED))




def schemes_tab(ui, lang):
    st.subheader(ui["sf_title"])
    st.caption(ui["sf_intro"])
    mode = st.radio(STEP_TEXT[lang]["mode"], ["step", "all"],
                    format_func=lambda m: STEP_TEXT[lang][m],
                    horizontal=True, key="sf_mode")
    answers = one_at_a_time(ui, lang) if mode == "step" else all_at_once(ui)
    if answers:
        show_results(ui, lang, answers)


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
