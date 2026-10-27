# schemes.py - schemes that MAY be worth checking, based on a few answers.
# This is NOT an eligibility decision. Rules change, so always send the person
# to the official site. To add a scheme: add its id to ORDER, a rule in
# find_schemes(), a link in LINKS and text in INFO for every language.
#
# Rules were last checked on LAST_CHECKED, from: the PM-KISAN official FAQ,
# a Karnataka district government page (Anna Bhagya), the Vikaspedia portal and
# news reports (Gruha Lakshmi, Gruha Jyothi, Shakti, Yuva Nidhi), and PM-JAY
# information. Where sources disagreed (Yuva Nidhi age limit) no hard rule is
# applied and the person is told to read the current notice.

LAST_CHECKED = "27 Oct 2026"

ORDER = ["gruha_lakshmi", "gruha_jyothi", "anna_bhagya", "shakti",
         "yuva_nidhi", "pmjay", "pmkisan"]

LINKS = {
    "gruha_lakshmi": "https://sevasindhugs.karnataka.gov.in/",
    "gruha_jyothi": "https://sevasindhugs.karnataka.gov.in/",
    "anna_bhagya": "https://ahara.kar.nic.in/",
    "shakti": "https://ksrtc.karnataka.gov.in",
    "yuva_nidhi": "https://sevasindhugs.karnataka.gov.in/",
    "pmjay": "https://pmjay.gov.in/",
    "pmkisan": "https://pmkisan.gov.in/",
}


def find_schemes(p):
    """p holds the answers: state (KA/OT), age, gender (W/M/O),
    ration (NONE/APL/BPL/AAY), and True/False flags woman_head, tax, govt,
    power, yuva, farm. Returns the ids of schemes worth checking."""
    ka = p["state"] == "KA"
    has_card = p["ration"] in ("APL", "BPL", "AAY")
    poor_card = p["ration"] in ("BPL", "AAY")
    hits = set()
    if ka and has_card and p["woman_head"] and not p["tax"]:
        hits.add("gruha_lakshmi")
    if ka and p["power"]:
        hits.add("gruha_jyothi")
    if ka and poor_card:
        hits.add("anna_bhagya")
    if ka and p["gender"] in ("W", "O"):
        hits.add("shakti")
    if ka and p["yuva"]:
        hits.add("yuva_nidhi")
    if p["age"] >= 70 or poor_card:
        hits.add("pmjay")
    if p["farm"] and not p["tax"] and not p["govt"]:
        hits.add("pmkisan")
    return [s for s in ORDER if s in hits]


INFO = {
    "English": {
        "gruha_lakshmi": {
            "name": "Gruha Lakshmi",
            "gives": "₹2,000 every month to the woman head of the family.",
            "check": "Your name must be recorded as head of the family on the ration card. Some sources also exclude government employees. Apply through Seva Sindhu.",
        },
        "gruha_jyothi": {
            "name": "Gruha Jyothi",
            "gives": "Free electricity up to 200 units a month for households.",
            "check": "It applies to home (domestic) connections, and tenants are included according to the state government. Register on Seva Sindhu.",
        },
        "anna_bhagya": {
            "name": "Anna Bhagya",
            "gives": "An extra 5 kg of free food grain per person each month, on top of the 5 kg from the central government.",
            "check": "The benefit comes through your BPL or Antyodaya ration card. The state's share has been paid as grain or as cash at different times.",
        },
        "shakti": {
            "name": "Shakti",
            "gives": "Free travel for women and transgender persons in ordinary (non-AC, non-luxury) state-run buses within Karnataka.",
            "check": "Carry a valid photo ID. A smart card is being introduced, so check the KSRTC website for the current rules.",
        },
        "yuva_nidhi": {
            "name": "Yuva Nidhi",
            "gives": "₹3,000 a month for unemployed graduates or ₹1,500 a month for diploma holders, for up to 2 years.",
            "check": "Sources differ on the age limit and the exact batch rules, so read the current notice on Seva Sindhu before applying.",
        },
        "pmjay": {
            "name": "Ayushman Bharat (PM-JAY)",
            "gives": "Free hospital treatment up to ₹5 lakh a year. Everyone aged 70 or more can get the Vay Vandana card, whatever their income.",
            "check": "If you are 70 or more, enrol with your Aadhaar. For other families, eligibility comes from a government list (SECC 2011), so check your name on the official site.",
        },
        "pmkisan": {
            "name": "PM-KISAN",
            "gives": "₹6,000 a year in three instalments for farmer families who own cultivable land.",
            "check": "The land must be in your family's name. A family is not eligible if any member paid income tax last year, and some government employees, pensioners and professionals are excluded. e-KYC is required.",
        },
    },
    "हिन्दी": {
        "gruha_lakshmi": {
            "name": "गृह लक्ष्मी",
            "gives": "परिवार की महिला मुखिया को हर महीने ₹2,000।",
            "check": "राशन कार्ड पर आपका नाम परिवार की मुखिया के रूप में दर्ज होना चाहिए। कुछ स्रोतों के अनुसार सरकारी कर्मचारी भी बाहर हैं। सेवा सिंधु से आवेदन करें।",
        },
        "gruha_jyothi": {
            "name": "गृह ज्योति",
            "gives": "घरों के लिए महीने में 200 यूनिट तक मुफ़्त बिजली।",
            "check": "यह घरेलू कनेक्शन पर लागू है, और राज्य सरकार के अनुसार किरायेदार भी शामिल हैं। सेवा सिंधु पर पंजीकरण करें।",
        },
        "anna_bhagya": {
            "name": "अन्न भाग्य",
            "gives": "केंद्र सरकार के 5 किलो के ऊपर, हर व्यक्ति को हर महीने 5 किलो अतिरिक्त मुफ़्त अनाज।",
            "check": "लाभ आपके BPL या अंत्योदय राशन कार्ड से मिलता है। राज्य का हिस्सा कभी अनाज के रूप में और कभी नकद के रूप में दिया गया है।",
        },
        "shakti": {
            "name": "शक्ति",
            "gives": "कर्नाटक के भीतर राज्य की साधारण (बिना AC, बिना लग्ज़री) बसों में महिलाओं और ट्रांसजेंडर व्यक्तियों के लिए मुफ़्त यात्रा।",
            "check": "मान्य फ़ोटो पहचान पत्र साथ रखें। स्मार्ट कार्ड शुरू किया जा रहा है, इसलिए मौजूदा नियमों के लिए KSRTC की वेबसाइट देखें।",
        },
        "yuva_nidhi": {
            "name": "युवा निधि",
            "gives": "बेरोज़गार स्नातकों को ₹3,000 प्रति माह या डिप्लोमा धारकों को ₹1,500 प्रति माह, अधिकतम 2 साल तक।",
            "check": "उम्र सीमा और बैच के नियमों के बारे में स्रोत अलग-अलग बताते हैं, इसलिए आवेदन से पहले सेवा सिंधु पर मौजूदा सूचना पढ़ें।",
        },
        "pmjay": {
            "name": "आयुष्मान भारत (PM-JAY)",
            "gives": "साल में ₹5 लाख तक मुफ़्त अस्पताल इलाज। 70 या अधिक उम्र के हर व्यक्ति को आय की परवाह किए बिना वय वंदना कार्ड मिल सकता है।",
            "check": "अगर आप 70 या उससे अधिक उम्र के हैं, तो आधार से नामांकन करें। दूसरे परिवारों की पात्रता सरकारी सूची (SECC 2011) से तय होती है, इसलिए सरकारी वेबसाइट पर अपना नाम देखें।",
        },
        "pmkisan": {
            "name": "पीएम-किसान",
            "gives": "खेती योग्य ज़मीन वाले किसान परिवारों को साल में तीन किस्तों में ₹6,000।",
            "check": "ज़मीन आपके परिवार के नाम पर होनी चाहिए। अगर परिवार के किसी भी सदस्य ने पिछले साल आयकर दिया है तो परिवार पात्र नहीं है, और कुछ सरकारी कर्मचारी, पेंशनभोगी और पेशेवर भी बाहर हैं। e-KYC ज़रूरी है।",
        },
    },
    "ಕನ್ನಡ": {
        "gruha_lakshmi": {
            "name": "ಗೃಹ ಲಕ್ಷ್ಮಿ",
            "gives": "ಕುಟುಂಬದ ಮಹಿಳಾ ಮುಖ್ಯಸ್ಥೆಗೆ ಪ್ರತಿ ತಿಂಗಳು ₹2,000.",
            "check": "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರಾಗಿ ದಾಖಲಾಗಿರಬೇಕು. ಕೆಲವು ಮೂಲಗಳ ಪ್ರಕಾರ ಸರ್ಕಾರಿ ನೌಕರರನ್ನೂ ಹೊರಗಿಡಲಾಗಿದೆ. ಸೇವಾ ಸಿಂಧು ಮೂಲಕ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
        },
        "gruha_jyothi": {
            "name": "ಗೃಹ ಜ್ಯೋತಿ",
            "gives": "ಮನೆಗಳಿಗೆ ತಿಂಗಳಿಗೆ 200 ಯೂನಿಟ್ ವರೆಗೆ ಉಚಿತ ವಿದ್ಯುತ್.",
            "check": "ಇದು ಮನೆಯ (ಗೃಹ) ಸಂಪರ್ಕಗಳಿಗೆ ಅನ್ವಯಿಸುತ್ತದೆ, ಮತ್ತು ರಾಜ್ಯ ಸರ್ಕಾರದ ಪ್ರಕಾರ ಬಾಡಿಗೆದಾರರೂ ಸೇರುತ್ತಾರೆ. ಸೇವಾ ಸಿಂಧುವಿನಲ್ಲಿ ನೋಂದಾಯಿಸಿ.",
        },
        "anna_bhagya": {
            "name": "ಅನ್ನ ಭಾಗ್ಯ",
            "gives": "ಕೇಂದ್ರ ಸರ್ಕಾರದ 5 ಕೆ.ಜಿ.ಗೆ ಹೆಚ್ಚುವರಿಯಾಗಿ, ಪ್ರತಿ ವ್ಯಕ್ತಿಗೆ ಪ್ರತಿ ತಿಂಗಳು 5 ಕೆ.ಜಿ. ಉಚಿತ ಆಹಾರಧಾನ್ಯ.",
            "check": "ಈ ಸೌಲಭ್ಯ ನಿಮ್ಮ BPL ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿಯ ಮೂಲಕ ಸಿಗುತ್ತದೆ. ರಾಜ್ಯದ ಪಾಲನ್ನು ಬೇರೆ ಬೇರೆ ಸಮಯದಲ್ಲಿ ಧಾನ್ಯವಾಗಿ ಅಥವಾ ನಗದಾಗಿ ನೀಡಲಾಗಿದೆ.",
        },
        "shakti": {
            "name": "ಶಕ್ತಿ",
            "gives": "ಕರ್ನಾಟಕದೊಳಗೆ ರಾಜ್ಯ ಸಾರಿಗೆ ಸಾಮಾನ್ಯ (ಎಸಿ ಅಲ್ಲದ, ಐಷಾರಾಮಿ ಅಲ್ಲದ) ಬಸ್ಸುಗಳಲ್ಲಿ ಮಹಿಳೆಯರು ಮತ್ತು ತೃತೀಯ ಲಿಂಗಿಗಳಿಗೆ ಉಚಿತ ಪ್ರಯಾಣ.",
            "check": "ಮಾನ್ಯ ಫೋಟೋ ಗುರುತಿನ ಚೀಟಿ ಜೊತೆಗಿರಲಿ. ಸ್ಮಾರ್ಟ್ ಕಾರ್ಡ್ ಜಾರಿಗೆ ಬರುತ್ತಿದೆ, ಆದ್ದರಿಂದ ಈಗಿನ ನಿಯಮಗಳಿಗೆ KSRTC ಜಾಲತಾಣ ನೋಡಿ.",
        },
        "yuva_nidhi": {
            "name": "ಯುವ ನಿಧಿ",
            "gives": "ನಿರುದ್ಯೋಗಿ ಪದವೀಧರರಿಗೆ ತಿಂಗಳಿಗೆ ₹3,000 ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಡೆದವರಿಗೆ ತಿಂಗಳಿಗೆ ₹1,500, ಗರಿಷ್ಠ 2 ವರ್ಷಗಳವರೆಗೆ.",
            "check": "ವಯಸ್ಸಿನ ಮಿತಿ ಮತ್ತು ಬ್ಯಾಚ್ ನಿಯಮಗಳ ಬಗ್ಗೆ ಮೂಲಗಳು ಬೇರೆ ಬೇರೆ ಹೇಳುತ್ತವೆ, ಆದ್ದರಿಂದ ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಸೇವಾ ಸಿಂಧುವಿನ ಈಗಿನ ಪ್ರಕಟಣೆ ಓದಿ.",
        },
        "pmjay": {
            "name": "ಆಯುಷ್ಮಾನ್ ಭಾರತ್ (PM-JAY)",
            "gives": "ವರ್ಷಕ್ಕೆ ₹5 ಲಕ್ಷದವರೆಗೆ ಉಚಿತ ಆಸ್ಪತ್ರೆ ಚಿಕಿತ್ಸೆ. 70 ವರ್ಷ ಅಥವಾ ಮೇಲ್ಪಟ್ಟ ಎಲ್ಲರೂ ಆದಾಯವನ್ನು ಲೆಕ್ಕಿಸದೆ ವಯ ವಂದನ ಕಾರ್ಡ್ ಪಡೆಯಬಹುದು.",
            "check": "ನಿಮಗೆ 70 ವರ್ಷ ಅಥವಾ ಮೇಲ್ಪಟ್ಟಿದ್ದರೆ ಆಧಾರ್ ಮೂಲಕ ನೋಂದಾಯಿಸಿ. ಇತರ ಕುಟುಂಬಗಳ ಅರ್ಹತೆ ಸರ್ಕಾರಿ ಪಟ್ಟಿಯಿಂದ (SECC 2011) ನಿರ್ಧಾರವಾಗುತ್ತದೆ, ಆದ್ದರಿಂದ ಅಧಿಕೃತ ಜಾಲತಾಣದಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ನೋಡಿ.",
        },
        "pmkisan": {
            "name": "ಪಿಎಂ-ಕಿಸಾನ್",
            "gives": "ಬೇಸಾಯ ಯೋಗ್ಯ ಭೂಮಿ ಹೊಂದಿರುವ ರೈತ ಕುಟುಂಬಗಳಿಗೆ ವರ್ಷಕ್ಕೆ ಮೂರು ಕಂತುಗಳಲ್ಲಿ ₹6,000.",
            "check": "ಭೂಮಿ ನಿಮ್ಮ ಕುಟುಂಬದ ಹೆಸರಿನಲ್ಲಿರಬೇಕು. ಕುಟುಂಬದ ಯಾರಾದರೂ ಕಳೆದ ವರ್ಷ ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿಸಿದ್ದರೆ ಕುಟುಂಬ ಅರ್ಹವಲ್ಲ, ಮತ್ತು ಕೆಲವು ಸರ್ಕಾರಿ ನೌಕರರು, ಪಿಂಚಣಿದಾರರು ಮತ್ತು ವೃತ್ತಿಪರರನ್ನೂ ಹೊರಗಿಡಲಾಗಿದೆ. e-KYC ಅಗತ್ಯ.",
        },
    },
}
