# test_explain.py - checks explain.py agrees with find_schemes() in schemes.py
# for EVERY combination of answers, and that no text is missing.
from itertools import product

from explain import (LABELS, MATCH_TEXT, RULES, TESTS, VERIFY, VERIFY_TEXT,
                     explain, scheme_applies)
from schemes import INFO, ORDER, find_schemes

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
assert set(RULES) == set(ORDER) == set(VERIFY)
print(f"OK: {count} answer combinations match find_schemes; all 3 languages complete.")
