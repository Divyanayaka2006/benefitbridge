# test_explain.py - checks explain.py agrees with find_schemes() in schemes.py
# for EVERY combination of answers, and that no text is missing.
from itertools import product

from explain import (LINK_FALLBACK, CHECKABLE, SUMMARY, build_summary, NO_LINK, DOC_FOOTER, DOC_LABEL, DOC_TEXT, DOCS, LABELS, MATCH_TEXT, RULES, TESTS, VERIFY, VERIFY_TEXT,
                     documents, explain, scheme_applies)
from schemes import INFO, LAST_CHECKED, LINKS, ORDER, find_schemes
from messages import TEXT
from steps import (ANSWER_KEYS, AUDIO_DIR, LANG_CODE, LISTEN, QUESTIONS,
                   STEP_TEXT)

count = 0
for state, age, gender, ration, wh, tax, govt, power, yuva, farm in product(
        ["KA", "OT"], [30, 69, 70, 90], ["W", "M", "O"],
        ["NONE", "APL", "BPL", "AAY"], *[[False, True]] * 6):
    p = dict(state=state, age=age, gender=gender, ration=ration,
             woman_head=wh, tax=tax, govt=govt, power=power, yuva=yuva, farm=farm)
    expected = find_schemes(p)
    got = [s for s in ORDER if scheme_applies(s, p)]
    assert got == expected, (p, got, expected)
    for sid in expected:
        matched, verify = explain(sid, p)
        assert matched, (sid, p)      # every shown scheme has a reason
        assert verify, (sid, p)       # and something to verify
    count += 1

for lang in INFO:
    assert lang in LABELS and lang in MATCH_TEXT and lang in VERIFY_TEXT, lang
    for k in TESTS:
        assert k in MATCH_TEXT[lang], (lang, k)
    for items in VERIFY.values():
        for v, _ in items:
            assert v in VERIFY_TEXT[lang], (lang, v)
    assert lang in DOC_LABEL and lang in DOC_FOOTER and lang in DOC_TEXT, lang
    for items in DOCS.values():
        for d, _ in items:
            assert d in DOC_TEXT[lang], (lang, d)
# one-question-at-a-time mode: covers every answer find_schemes needs, and
# every language has every text
assert [q["key"] for q in QUESTIONS] == ANSWER_KEYS
for lang in INFO:
    assert lang in STEP_TEXT, lang
    for k in ["mode", "step", "all", "progress", "yes", "no", "back", "next", "restart"]:
        assert k in STEP_TEXT[lang], (lang, k)
    for q in QUESTIONS:
        if "text" in q:
            assert q["text"] in STEP_TEXT[lang], (lang, q["text"])
        else:
            assert q["ui"] in TEXT[lang]["ui"], (lang, q["ui"])
        for opt in q.get("options", []):
            assert "o_" + opt in TEXT[lang]["ui"], (lang, opt)
for lang in INFO:
    assert lang in LANG_CODE and lang in AUDIO_DIR and lang in LISTEN, lang
    assert {"listen", "no_voice"} <= set(LISTEN[lang]), lang
assert set(LINKS) <= set(ORDER)
assert all(lang in LINK_FALLBACK for lang in INFO)
assert all(d in next(iter(DOC_TEXT.values())) for d in CHECKABLE)
# the summary builds in every language, ticks show up, nothing crashes
p = dict(state="KA", age=75, gender="W", ration="BPL", woman_head=True,
         tax=False, govt=False, power=True, yuva=False, farm=True)
hits = find_schemes(p)
for lang in INFO:
    ui = TEXT[lang]["ui"]
    none = build_summary(lang, ui, hits, p, set(), INFO, LINKS, LAST_CHECKED)
    allx = {(s, d) for s in hits for d in DOC_TEXT[lang] if d in CHECKABLE}
    some = build_summary(lang, ui, hits, p, allx, INFO, LINKS, LAST_CHECKED)
    assert INFO[lang][hits[0]]["name"] in none
    assert "[ ]" in none and "[x]" not in none
    assert "[x]" in some and SUMMARY[lang]["none_left"] in some
assert set(LINKS) <= set(ORDER)
assert all(lang in NO_LINK for lang in INFO)
assert set(RULES) == set(ORDER) == set(VERIFY) == set(DOCS)
print(f"OK: {count} answer combinations match find_schemes; all 3 languages complete.")
