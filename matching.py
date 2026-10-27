# matching.py - turn typed text into the match scores the model expects.
# Uses only the Python standard library, so nothing extra needs installing.
import string
from difflib import SequenceMatcher

# Replace ASCII punctuation with spaces. Letters of every language
# (including Hindi and Kannada vowel signs) are left untouched.
_PUNCT = str.maketrans({c: " " for c in string.punctuation})


def _clean(text):
    return " ".join(str(text).lower().translate(_PUNCT).split())


def match_score(a, b):
    """Similarity from 0.0 to 1.0. Ignores case, punctuation and word order.
    Returns 0.0 when either text is empty."""
    a, b = _clean(a), _clean(b)
    if not a or not b:
        return 0.0
    a = " ".join(sorted(a.split()))
    b = " ".join(sorted(b.split()))
    return SequenceMatcher(None, a, b).ratio()


def income_gap(on_form, on_proof):
    """Fractional difference between the income on the form and on the proof."""
    if on_proof <= 0:
        return 0.0 if on_form <= 0 else 1.0
    return min(abs(on_form - on_proof) / on_proof, 1.0)
