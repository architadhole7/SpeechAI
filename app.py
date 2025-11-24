import re
import os
from collections import Counter
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from flask import Flask, render_template, request, jsonify


# FLASK APP

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# INITIALIZATION og Language tool

tool = language_tool_python.LanguageTool('en-US')
VADER = SentimentIntensityAnalyzer()

# Filler words
FILLER_WORDS = {
    "um","uh","like","you know","so","actually","basically","right","i mean",
    "well","kinda","sort of","okay","hmm","ah","erm","mm"
}


# 1. SALUTATION (0–5)

def score_salutation(text):
    t = text.lower()
    strong = ["i am excited to introduce", "feeling great"]
    good = ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]
    normal = ["hello", "hi"]

    for s in strong:
        if s in t: return 5
    for s in good:
        if s in t: return 4
    for s in normal:
        if re.search(r'\b' + re.escape(s) + r'\b', t): return 2
    return 0

# 2. KEYWORDS (0–30)

def score_keywords(text):
    t = text.lower()
    score = 0
    detail = {"must":[],"good":[]}

    MUST = {
        "name": [r"\b[a-zA-Z]+ [a-zA-Z]+\b", r"my name is", r"myself", r"i am"],
        "age": [r"\bage \d{1,2}\b", r"\bi am \d{1,2}\b", r"\d{1,2} years old"],
        "class_school": [r"class", r"grade", r"section", r"school"],
        "family": [r"family", r"father", r"mother", r"parents", r"sibling"],
        "hobby": [r"hobby", r"i enjoy", r"i like", r"favourite", r"favorite"]
    }

    GOOD = {
        "origin": [r"i am from", r"i'm from", r"parents are from"],
        "goal": [r"goal", r"ambition", r"want to be", r"dream"],
        "fun_fact": [r"fun fact", r"one thing people", r"interesting thing"],
        "achievement": [r"achievement", r"prize", r"won"],
        "unique": [r"unique", r"special"]
    }

    # Must-have scoring
    for key, patterns in MUST.items():
        for p in patterns:
            if re.search(p, t):
                detail["must"].append(key)
                score += 4
                break

    # Good-to-have scoring
    for key, patterns in GOOD.items():
        for p in patterns:
            if re.search(p, t):
                detail["good"].append(key)
                score += 2
                break

    return min(score, 30), detail

# Scoring Logic

# 3. FLOW (0–5)

def score_flow(text):
    t = text.lower()
    order_patterns = [
        r"(hello|hi|good morning|good afternoon|good evening|good day|hello everyone)",
        r"\b[a-zA-Z]+ [a-zA-Z]+\b",  # name
        r"age \d{1,2}|\bi am \d{1,2}\b",
        r"(family|father|mother|parents|sibling)",
        r"(goal|ambition|dream|hobby|fun fact|unique|interesting thing)",
        r"(thank you|thanks)"
    ]
    positions = []
    for i, pattern in enumerate(order_patterns):
        m = re.search(pattern, t)
        if m:
            positions.append((i, m.start()))
    if not positions: return 0
    pos_only = [p[1] for p in positions]
    return 5 if pos_only == sorted(pos_only) else 3


# 4. WPM (0–10)

def score_wpm(wpm):
    if 111 <= wpm <= 140: return 10
    if 141 <= wpm <= 160: return 6
    if wpm > 160: return 2
    if 81 <= wpm <= 110: return 6
    return 2

# 5. GRAMMAR (0–10)

def score_grammar(text):
    matches = tool.check(text)
    errors = len(matches)
    words = max(1, len(re.findall(r"\w+", text)))
    err_per_100 = (errors / words) * 100

    if err_per_100 > 90: return 10, 1 - err_per_100/100
    if err_per_100 >= 70: return 8, 1 - err_per_100/100
    if err_per_100 >= 50: return 6, 1 - err_per_100/100
    if err_per_100 >= 30: return 4, 1 - err_per_100/100
    return 2, 1 - err_per_100/100


# 6. VOCAB (0–10)

def score_ttr(text):
    tokens = re.findall(r"\w+", text.lower())
    total = len(tokens)
    unique = len(set(tokens))
    ttr = unique / total if total else 0
    if ttr >= 0.9: return 10, ttr
    if ttr >= 0.7: return 8, ttr
    if ttr >= 0.5: return 6, ttr
    if ttr >= 0.3: return 4, ttr
    return 2, ttr


# 7. FILLER WORDS (0–15)

def score_filler(text):
    t = text.lower()
    words = re.findall(r"\w+", t)
    total = len(words)
    count = 0
    found = Counter()
    for fw in FILLER_WORDS:
        n = len(re.findall(r'\b'+fw+r'\b', t))
        if n>0: found[fw]=n
        count += n
    rate = (count/total)*100 if total>0 else 0
    if rate <= 3: return 15, rate, found
    if rate <= 6: return 12, rate, found
    if rate <= 9: return 9, rate, found
    if rate <= 12: return 6, rate, found
    return 3, rate, found

# 8. SENTIMENT (0–15)

def score_sentiment(text):
    scores = VADER.polarity_scores(text)
    pos = scores["pos"]
    if pos >= 0.9: return 15, pos
    if pos >= 0.7: return 12, pos
    if pos >= 0.5: return 9, pos
    if pos >= 0.3: return 6, pos
    return 3, pos


# FINAL SCORE AGGREGATION

def compute_scores(text, wpm):
    salutation = score_salutation(text)
    keywords, keywords_detail = score_keywords(text)
    flow = score_flow(text)
    wpm_score = score_wpm(wpm)
    grammar_score, grammar_quality = score_grammar(text)
    vocab_score, vocab_value = score_ttr(text)
    filler_score, filler_rate, filler_found = score_filler(text)
    sentiment_score, sentiment_value = score_sentiment(text)

    overall = salutation + keywords + flow + wpm_score + grammar_score + vocab_score + filler_score + sentiment_score

    return {
        "Total Score": f"{overall}/100",
        "salutation": salutation,
        "keywords": keywords,
        "keywords_detail": keywords_detail,
        "flow": flow,
        "wpm": wpm_score,
        "grammar": grammar_score,
        "vocab": vocab_score,
        "filler": filler_score,
        "sentiment": sentiment_score,
        "overall": overall
    }

# ROUTES

@app.route("/score", methods=["POST"])
def score():
    data = request.get_json(force=True)
    text = data.get("text", "")
    wpm = data.get("wpm", 120)
    results = compute_scores(text, wpm)
    return jsonify(results)


# Run Program
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
