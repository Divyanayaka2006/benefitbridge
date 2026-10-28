# steps.py - the questions for "one question at a time" mode.
# Same ten answers as the all-at-once form, so find_schemes() is unchanged.
# Nothing is saved: answers live only in this browser session.

# kind: "choice" = one big button per option, "yesno" = Yes / No, "number" = age
# "ui" = reuse a question already in messages.py, "text" = key in STEP_TEXT below
QUESTIONS = [
    {"key": "state", "kind": "choice", "options": ["KA", "OT"], "icon": "📍", "ui": "sf_state"},
    {"key": "age", "kind": "number", "icon": "🎂", "text": "q_age"},
    {"key": "gender", "kind": "choice", "options": ["W", "M", "O"], "icon": "👤", "ui": "sf_gender"},
    {"key": "ration", "kind": "choice", "options": ["NONE", "APL", "BPL", "AAY"], "icon": "🪪", "ui": "sf_ration"},
    {"key": "woman_head", "kind": "yesno", "icon": "👩‍👧", "text": "q_head"},
    {"key": "tax", "kind": "yesno", "icon": "🧾", "text": "q_tax"},
    {"key": "govt", "kind": "yesno", "icon": "🏢", "text": "q_govt"},
    {"key": "power", "kind": "yesno", "icon": "💡", "text": "q_power"},
    {"key": "yuva", "kind": "yesno", "icon": "🎓", "text": "q_yuva"},
    {"key": "farm", "kind": "yesno", "icon": "🌾", "text": "q_farm"},
]

# The answer keys find_schemes() needs. The test checks QUESTIONS covers them.
ANSWER_KEYS = ["state", "age", "gender", "ration", "woman_head", "tax",
               "govt", "power", "yuva", "farm"]

STEP_TEXT = {
    "English": {
        "mode": "How do you want to answer?",
        "step": "One question at a time",
        "all": "All questions at once",
        "progress": "Question {n} of {total}",
        "yes": "Yes", "no": "No",
        "back": "Back", "next": "Next",
        "restart": "Start again",
        "q_age": "How old are you?",
        "q_head": "Are you the woman head of the family on your ration card?",
        "q_tax": "Do you or your spouse pay income tax or file GST returns?",
        "q_govt": "Do you or your spouse have a government job?",
        "q_power": "Does your home have a household electricity connection that uses 200 units or less a month?",
        "q_yuva": "Did you pass a degree or diploma in 2022-23 or later, and are you unemployed?",
        "q_farm": "Does your family own farmland in your names?",
    },
    "हिन्दी": {
        "mode": "आप कैसे जवाब देना चाहते हैं?",
        "step": "एक-एक सवाल",
        "all": "सभी सवाल एक साथ",
        "progress": "प्रश्न {n} / {total}",
        "yes": "हाँ", "no": "नहीं",
        "back": "पीछे", "next": "आगे",
        "restart": "फिर से शुरू करें",
        "q_age": "आपकी उम्र कितनी है?",
        "q_head": "क्या आप राशन कार्ड पर परिवार की महिला मुखिया हैं?",
        "q_tax": "क्या आप या आपके जीवनसाथी आयकर देते हैं या GST रिटर्न भरते हैं?",
        "q_govt": "क्या आप या आपके जीवनसाथी सरकारी नौकरी में हैं?",
        "q_power": "क्या आपके घर में घरेलू बिजली कनेक्शन है और महीने में 200 यूनिट या कम बिजली लगती है?",
        "q_yuva": "क्या आपने 2022-23 या उसके बाद डिग्री या डिप्लोमा पास किया है और आप बेरोज़गार हैं?",
        "q_farm": "क्या आपके परिवार के नाम पर खेती की ज़मीन है?",
    },
    "ಕನ್ನಡ": {
        "mode": "ನೀವು ಹೇಗೆ ಉತ್ತರಿಸಲು ಬಯಸುತ್ತೀರಿ?",
        "step": "ಒಂದೊಂದು ಪ್ರಶ್ನೆ",
        "all": "ಎಲ್ಲ ಪ್ರಶ್ನೆಗಳು ಒಂದೇ ಬಾರಿ",
        "progress": "ಪ್ರಶ್ನೆ {n} / {total}",
        "yes": "ಹೌದು", "no": "ಇಲ್ಲ",
        "back": "ಹಿಂದೆ", "next": "ಮುಂದೆ",
        "restart": "ಮತ್ತೆ ಶುರು ಮಾಡಿ",
        "q_age": "ನಿಮ್ಮ ವಯಸ್ಸು ಎಷ್ಟು?",
        "q_head": "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ ನೀವು ಕುಟುಂಬದ ಮಹಿಳಾ ಮುಖ್ಯಸ್ಥೆಯೇ?",
        "q_tax": "ನೀವು ಅಥವಾ ನಿಮ್ಮ ಸಂಗಾತಿ ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿಸುತ್ತೀರಾ ಅಥವಾ GST ರಿಟರ್ನ್ ಸಲ್ಲಿಸುತ್ತೀರಾ?",
        "q_govt": "ನೀವು ಅಥವಾ ನಿಮ್ಮ ಸಂಗಾತಿ ಸರ್ಕಾರಿ ಉದ್ಯೋಗದಲ್ಲಿದ್ದೀರಾ?",
        "q_power": "ನಿಮ್ಮ ಮನೆಗೆ ಗೃಹ ವಿದ್ಯುತ್ ಸಂಪರ್ಕವಿದೆಯೇ ಮತ್ತು ತಿಂಗಳಿಗೆ 200 ಯೂನಿಟ್ ಅಥವಾ ಕಡಿಮೆ ಬಳಸುತ್ತೀರಾ?",
        "q_yuva": "2022-23 ಅಥವಾ ನಂತರ ನೀವು ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಾಸಾಗಿ ನಿರುದ್ಯೋಗಿಯಾಗಿದ್ದೀರಾ?",
        "q_farm": "ನಿಮ್ಮ ಕುಟುಂಬದ ಹೆಸರಿನಲ್ಲಿ ಕೃಷಿ ಭೂಮಿ ಇದೆಯೇ?",
    },
}


# ---------------------------------------------------------------------------
# Read-aloud ("Listen") buttons. Only FIXED text is spoken: questions, scheme
# names and what a scheme gives. The person's own answers are never spoken or
# sent anywhere.
#
# If a file audio/<dir>/<id>.mp3 exists (a real recording, or audio made ahead
# of time) it is played. Otherwise the device's own voice is used in the
# browser. ids: q_state, q_age, q_gender, ... and scheme_<scheme id>.
LANG_CODE = {"English": "en-IN", "हिन्दी": "hi-IN", "ಕನ್ನಡ": "kn-IN"}
AUDIO_DIR = {"English": "en", "हिन्दी": "hi", "ಕನ್ನಡ": "kn"}

LISTEN = {
    "English": {"listen": "Listen",
                "no_voice": "This device has no voice for this language."},
    "हिन्दी": {"listen": "सुनें",
               "no_voice": "इस डिवाइस में इस भाषा की आवाज़ नहीं है।"},
    "ಕನ್ನಡ": {"listen": "ಕೇಳಿ",
              "no_voice": "ಈ ಸಾಧನದಲ್ಲಿ ಈ ಭಾಷೆಯ ಧ್ವನಿ ಇಲ್ಲ."},
}
