# explain.py - explains WHY a scheme appeared, using the same rules as
# find_schemes() in schemes.py. Nothing here is written by an AI model at
# run time: every sentence below is fixed text, chosen by the answers.
#
# Three kinds of information for each scheme:
#   matched : conditions from the user's answers that were true
#   verify  : things the app cannot know, so the user must check them
#   (the official link is already shown by app.py)
#
# If you change a rule in find_schemes(), change RULES below too.
# Run "python test_explain.py" to check the two still agree.

# Each test looks at the answers dictionary p (same keys as find_schemes).
TESTS = {
    "in_ka": lambda p: p["state"] == "KA",
    "has_card": lambda p: p["ration"] in ("APL", "BPL", "AAY"),
    "poor_card": lambda p: p["ration"] in ("BPL", "AAY"),
    "woman_head": lambda p: p["woman_head"],
    "no_tax": lambda p: not p["tax"],
    "no_govt": lambda p: not p["govt"],
    "power": lambda p: p["power"],
    "gender_wo": lambda p: p["gender"] in ("W", "O"),
    "yuva": lambda p: p["yuva"],
    "age70": lambda p: p["age"] >= 70,
    "farm": lambda p: p["farm"],
}

# "all" = every condition must be true. "any" = at least one must be true.
RULES = {
    "gruha_lakshmi": {"all": ["in_ka", "has_card", "woman_head", "no_tax"]},
    "gruha_jyothi": {"all": ["in_ka", "power"]},
    "anna_bhagya": {"all": ["in_ka", "poor_card"]},
    "shakti": {"all": ["in_ka", "gender_wo"]},
    "yuva_nidhi": {"all": ["in_ka", "yuva"]},
    "pmjay": {"any": ["age70", "poor_card"]},
    "pmkisan": {"all": ["farm", "no_tax", "no_govt"]},
}

# Things the user must verify. Each item is (verify_key, only_if_matched).
# only_if_matched is None (always show) or a matched-condition key.
VERIFY = {
    "gruha_lakshmi": [("head_on_card", None), ("govt_excl", None)],
    "gruha_jyothi": [("domestic", None)],
    "anna_bhagya": [("anna_form", None)],
    "shakti": [("shakti_bus", None)],
    "yuva_nidhi": [("yuva_rules", None)],
    "pmjay": [("pmjay_age", "age70"), ("pmjay_secc", "poor_card")],
    "pmkisan": [("pmk_land", None), ("pmk_family_tax", None),
                ("pmk_excl", None), ("pmk_ekyc", None)],
}


def explain(sid, p):
    """Return (matched_keys, verify_keys) for scheme sid and answers p."""
    rule = RULES[sid]
    if "all" in rule:
        matched = [k for k in rule["all"] if TESTS[k](p)]
    else:
        matched = [k for k in rule["any"] if TESTS[k](p)]
    verify = [v for v, needs in VERIFY[sid] if needs is None or needs in matched]
    return matched, verify


def scheme_applies(sid, p):
    """True if the rules in RULES say this scheme should appear."""
    rule = RULES[sid]
    if "all" in rule:
        return all(TESTS[k](p) for k in rule["all"])
    return any(TESTS[k](p) for k in rule["any"])


LABELS = {
    "English": {
        "why": "Why this appeared",
        "verify": "Still to verify before you apply",
    },
    "हिन्दी": {
        "why": "यह क्यों दिखा",
        "verify": "आवेदन से पहले जाँचने योग्य बातें",
    },
    "ಕನ್ನಡ": {
        "why": "ಇದು ಏಕೆ ಕಾಣಿಸಿತು",
        "verify": "ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಪರಿಶೀಲಿಸಬೇಕಾದವು",
    },
}

MATCH_TEXT = {
    "English": {
        "in_ka": "You live in Karnataka.",
        "has_card": "You have a ration card (APL, BPL or Antyodaya).",
        "poor_card": "You have a BPL or Antyodaya ration card.",
        "woman_head": "You said you are the woman head of the family on the ration card.",
        "no_tax": "You said you and your spouse do not pay income tax or file GST returns.",
        "no_govt": "You said you and your spouse do not work in a government job.",
        "power": "You said your home has a household electricity connection using 200 units or less a month.",
        "gender_wo": "You said you are a woman or another gender (including transgender).",
        "yuva": "You said you passed a degree or diploma in 2022-23 or later and are unemployed.",
        "age70": "Your age is 70 or more.",
        "farm": "You said your family owns farmland in your names.",
    },
    "हिन्दी": {
        "in_ka": "आप कर्नाटक में रहते हैं।",
        "has_card": "आपके पास राशन कार्ड है (APL, BPL या अंत्योदय)।",
        "poor_card": "आपके पास BPL या अंत्योदय राशन कार्ड है।",
        "woman_head": "आपने बताया कि आप राशन कार्ड पर परिवार की महिला मुखिया हैं।",
        "no_tax": "आपने बताया कि आप या आपके जीवनसाथी आयकर नहीं देते और GST रिटर्न नहीं भरते।",
        "no_govt": "आपने बताया कि आप या आपके जीवनसाथी सरकारी नौकरी में नहीं हैं।",
        "power": "आपने बताया कि आपके घर में घरेलू बिजली कनेक्शन है और महीने में 200 यूनिट या कम बिजली लगती है।",
        "gender_wo": "आपने बताया कि आप महिला या अन्य लिंग (ट्रांसजेंडर सहित) हैं।",
        "yuva": "आपने बताया कि आपने 2022-23 या उसके बाद डिग्री या डिप्लोमा पास किया है और आप बेरोज़गार हैं।",
        "age70": "आपकी उम्र 70 या उससे अधिक है।",
        "farm": "आपने बताया कि आपके परिवार के नाम पर खेती की ज़मीन है।",
    },
    "ಕನ್ನಡ": {
        "in_ka": "ನೀವು ಕರ್ನಾಟಕದಲ್ಲಿ ವಾಸಿಸುತ್ತೀರಿ.",
        "has_card": "ನಿಮ್ಮ ಬಳಿ ಪಡಿತರ ಚೀಟಿ ಇದೆ (APL, BPL ಅಥವಾ ಅಂತ್ಯೋದಯ).",
        "poor_card": "ನಿಮ್ಮ ಬಳಿ BPL ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿ ಇದೆ.",
        "woman_head": "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ ನೀವು ಕುಟುಂಬದ ಮಹಿಳಾ ಮುಖ್ಯಸ್ಥೆ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "no_tax": "ನೀವು ಅಥವಾ ನಿಮ್ಮ ಸಂಗಾತಿ ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿಸುವುದಿಲ್ಲ ಅಥವಾ GST ರಿಟರ್ನ್ ಸಲ್ಲಿಸುವುದಿಲ್ಲ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "no_govt": "ನೀವು ಅಥವಾ ನಿಮ್ಮ ಸಂಗಾತಿ ಸರ್ಕಾರಿ ಉದ್ಯೋಗದಲ್ಲಿಲ್ಲ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "power": "ನಿಮ್ಮ ಮನೆಗೆ ಗೃಹ ವಿದ್ಯುತ್ ಸಂಪರ್ಕವಿದೆ ಮತ್ತು ತಿಂಗಳಿಗೆ 200 ಯೂನಿಟ್ ಅಥವಾ ಕಡಿಮೆ ಬಳಸುತ್ತೀರಿ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "gender_wo": "ನೀವು ಮಹಿಳೆ ಅಥವಾ ಇತರ ಲಿಂಗ (ತೃತೀಯ ಲಿಂಗಿ ಸೇರಿ) ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "yuva": "2022-23 ಅಥವಾ ನಂತರ ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಾಸಾಗಿ ನಿರುದ್ಯೋಗಿಯಾಗಿದ್ದೀರಿ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
        "age70": "ನಿಮ್ಮ ವಯಸ್ಸು 70 ಅಥವಾ ಹೆಚ್ಚು.",
        "farm": "ನಿಮ್ಮ ಕುಟುಂಬದ ಹೆಸರಿನಲ್ಲಿ ಕೃಷಿ ಭೂಮಿ ಇದೆ ಎಂದು ತಿಳಿಸಿದ್ದೀರಿ.",
    },
}

VERIFY_TEXT = {
    "English": {
        "head_on_card": "Your name must be recorded as head of the family on the ration card. Look at the card itself to confirm.",
        "govt_excl": "Some sources also exclude government employees, so check the current official conditions.",
        "domestic": "It applies to home (domestic) connections. Confirm with your electricity bill or electricity company that your connection is a home connection.",
        "anna_form": "The state's share has been paid as grain or as cash at different times, so check how it is being given now.",
        "shakti_bus": "Free travel is for ordinary (non-AC, non-luxury) state-run buses. Carry a valid photo ID and check the KSRTC website for the current rules.",
        "yuva_rules": "Sources differ on the age limit and the exact batch rules, so we cannot say whether you meet them. Read the current notice on Seva Sindhu.",
        "pmjay_age": "If you are 70 or more, enrol with your Aadhaar for the Vay Vandana card.",
        "pmjay_secc": "A BPL or Antyodaya card alone does not confirm eligibility. For other families, eligibility comes from a government list (SECC 2011), so check your name on the official site.",
        "pmk_land": "The land must be in your family's name. Check the land records.",
        "pmk_family_tax": "We asked only about you and your spouse. A family is not eligible if any member paid income tax last year, so check other family members too.",
        "pmk_excl": "Some government employees, pensioners and professionals are excluded. Check the current exclusions on the official site.",
        "pmk_ekyc": "e-KYC is required.",
    },
    "हिन्दी": {
        "head_on_card": "राशन कार्ड पर आपका नाम परिवार की मुखिया के रूप में दर्ज होना चाहिए। पुष्टि के लिए कार्ड खुद देखें।",
        "govt_excl": "कुछ स्रोतों के अनुसार सरकारी कर्मचारी भी बाहर हैं, इसलिए मौजूदा सरकारी शर्तें जाँचें।",
        "domestic": "यह घरेलू कनेक्शन पर लागू है। अपने बिजली बिल या बिजली कंपनी से पुष्टि करें कि आपका कनेक्शन घरेलू है।",
        "anna_form": "राज्य का हिस्सा कभी अनाज के रूप में और कभी नकद के रूप में दिया गया है, इसलिए जाँचें कि अभी कैसे दिया जा रहा है।",
        "shakti_bus": "मुफ़्त यात्रा राज्य की साधारण (बिना AC, बिना लग्ज़री) बसों में है। मान्य फ़ोटो पहचान पत्र साथ रखें और मौजूदा नियमों के लिए KSRTC की वेबसाइट देखें।",
        "yuva_rules": "उम्र सीमा और बैच के नियमों के बारे में स्रोत अलग-अलग बताते हैं, इसलिए हम नहीं कह सकते कि आप इन्हें पूरा करते हैं या नहीं। सेवा सिंधु पर मौजूदा सूचना पढ़ें।",
        "pmjay_age": "अगर आप 70 या उससे अधिक उम्र के हैं, तो वय वंदना कार्ड के लिए आधार से नामांकन करें।",
        "pmjay_secc": "केवल BPL या अंत्योदय कार्ड से पात्रता पक्की नहीं होती। दूसरे परिवारों की पात्रता सरकारी सूची (SECC 2011) से तय होती है, इसलिए सरकारी वेबसाइट पर अपना नाम देखें।",
        "pmk_land": "ज़मीन आपके परिवार के नाम पर होनी चाहिए। ज़मीन के रिकॉर्ड जाँचें।",
        "pmk_family_tax": "हमने केवल आपके और आपके जीवनसाथी के बारे में पूछा है। अगर परिवार के किसी भी सदस्य ने पिछले साल आयकर दिया है तो परिवार पात्र नहीं है, इसलिए परिवार के दूसरे सदस्यों के बारे में भी जाँचें।",
        "pmk_excl": "कुछ सरकारी कर्मचारी, पेंशनभोगी और पेशेवर बाहर हैं। सरकारी वेबसाइट पर मौजूदा बहिष्करण जाँचें।",
        "pmk_ekyc": "e-KYC ज़रूरी है।",
    },
    "ಕನ್ನಡ": {
        "head_on_card": "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರಾಗಿ ದಾಖಲಾಗಿರಬೇಕು. ಖಚಿತಪಡಿಸಲು ಚೀಟಿಯನ್ನೇ ನೋಡಿ.",
        "govt_excl": "ಕೆಲವು ಮೂಲಗಳ ಪ್ರಕಾರ ಸರ್ಕಾರಿ ನೌಕರರನ್ನೂ ಹೊರಗಿಡಲಾಗಿದೆ, ಆದ್ದರಿಂದ ಈಗಿನ ಅಧಿಕೃತ ಷರತ್ತುಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "domestic": "ಇದು ಮನೆಯ (ಗೃಹ) ಸಂಪರ್ಕಗಳಿಗೆ ಅನ್ವಯಿಸುತ್ತದೆ. ನಿಮ್ಮ ಸಂಪರ್ಕ ಗೃಹ ಸಂಪರ್ಕವೇ ಎಂದು ವಿದ್ಯುತ್ ಬಿಲ್ ಅಥವಾ ವಿದ್ಯುತ್ ಕಂಪನಿಯಿಂದ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
        "anna_form": "ರಾಜ್ಯದ ಪಾಲನ್ನು ಬೇರೆ ಬೇರೆ ಸಮಯದಲ್ಲಿ ಧಾನ್ಯವಾಗಿ ಅಥವಾ ನಗದಾಗಿ ನೀಡಲಾಗಿದೆ, ಆದ್ದರಿಂದ ಈಗ ಹೇಗೆ ನೀಡಲಾಗುತ್ತಿದೆ ಎಂದು ಪರಿಶೀಲಿಸಿ.",
        "shakti_bus": "ಉಚಿತ ಪ್ರಯಾಣ ರಾಜ್ಯ ಸಾರಿಗೆಯ ಸಾಮಾನ್ಯ (ಎಸಿ ಅಲ್ಲದ, ಐಷಾರಾಮಿ ಅಲ್ಲದ) ಬಸ್ಸುಗಳಲ್ಲಿ ಮಾತ್ರ. ಮಾನ್ಯ ಫೋಟೋ ಗುರುತಿನ ಚೀಟಿ ಜೊತೆಗಿರಲಿ ಮತ್ತು ಈಗಿನ ನಿಯಮಗಳಿಗೆ KSRTC ಜಾಲತಾಣ ನೋಡಿ.",
        "yuva_rules": "ವಯಸ್ಸಿನ ಮಿತಿ ಮತ್ತು ಬ್ಯಾಚ್ ನಿಯಮಗಳ ಬಗ್ಗೆ ಮೂಲಗಳು ಬೇರೆ ಬೇರೆ ಹೇಳುತ್ತವೆ, ಆದ್ದರಿಂದ ನೀವು ಅವುಗಳನ್ನು ಪೂರೈಸುತ್ತೀರಿ ಎಂದು ನಾವು ಹೇಳಲಾಗದು. ಸೇವಾ ಸಿಂಧುವಿನ ಈಗಿನ ಪ್ರಕಟಣೆ ಓದಿ.",
        "pmjay_age": "ನಿಮಗೆ 70 ವರ್ಷ ಅಥವಾ ಮೇಲ್ಪಟ್ಟಿದ್ದರೆ ವಯ ವಂದನ ಕಾರ್ಡ್‌ಗಾಗಿ ಆಧಾರ್ ಮೂಲಕ ನೋಂದಾಯಿಸಿ.",
        "pmjay_secc": "ಕೇವಲ BPL ಅಥವಾ ಅಂತ್ಯೋದಯ ಚೀಟಿಯಿಂದ ಅರ್ಹತೆ ಖಚಿತವಾಗುವುದಿಲ್ಲ. ಇತರ ಕುಟುಂಬಗಳ ಅರ್ಹತೆ ಸರ್ಕಾರಿ ಪಟ್ಟಿಯಿಂದ (SECC 2011) ನಿರ್ಧಾರವಾಗುತ್ತದೆ, ಆದ್ದರಿಂದ ಅಧಿಕೃತ ಜಾಲತಾಣದಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ನೋಡಿ.",
        "pmk_land": "ಭೂಮಿ ನಿಮ್ಮ ಕುಟುಂಬದ ಹೆಸರಿನಲ್ಲಿರಬೇಕು. ಭೂ ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "pmk_family_tax": "ನಾವು ನಿಮ್ಮ ಮತ್ತು ನಿಮ್ಮ ಸಂಗಾತಿಯ ಬಗ್ಗೆ ಮಾತ್ರ ಕೇಳಿದ್ದೇವೆ. ಕುಟುಂಬದ ಯಾರಾದರೂ ಕಳೆದ ವರ್ಷ ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿಸಿದ್ದರೆ ಕುಟುಂಬ ಅರ್ಹವಲ್ಲ, ಆದ್ದರಿಂದ ಕುಟುಂಬದ ಇತರ ಸದಸ್ಯರ ಬಗ್ಗೆಯೂ ಪರಿಶೀಲಿಸಿ.",
        "pmk_excl": "ಕೆಲವು ಸರ್ಕಾರಿ ನೌಕರರು, ಪಿಂಚಣಿದಾರರು ಮತ್ತು ವೃತ್ತಿಪರರನ್ನು ಹೊರಗಿಡಲಾಗಿದೆ. ಅಧಿಕೃತ ಜಾಲತಾಣದಲ್ಲಿ ಈಗಿನ ಹೊರಗಿಡುವಿಕೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "pmk_ekyc": "e-KYC ಅಗತ್ಯ.",
    },
}
