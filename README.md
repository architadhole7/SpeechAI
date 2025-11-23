# SpeechAI

# Speech Scoring App

This is a **Flask-based web application** that scores speech transcripts automatically based on a detailed rubric. The app analyzes the text for **content, structure, grammar, clarity, engagement, and speech rate** and produces a score out of 100.

---

## Features

- Upload or type a speech transcript directly in the web interface.
- Calculate **word count, sentence count, and estimated speech duration**.
- Automatic scoring based on a **predefined rubric** covering:
  - **Content & Structure**  
  - **Speech Rate (Words per Minute)**  
  - **Language & Grammar**  
  - **Vocabulary Richness (TTR)**  
  - **Clarity (Filler words)**  
  - **Engagement (Sentiment analysis using VADER)**
- Returns detailed **JSON output** with individual criterion scores and total score.
- Fully client-server interactive using Flask.

---

## Files

**app.py**	                Main Flask application handling scoring logic and API routes
**templates/index.html**	Frontend HTML interface
**static/styles.css**	    CSS styling for the frontend
**requirements.txt**	    Python dependencies

---

## Scoring Rubric

The speech is scored across six main criteria:

1. Content & Structure (40 points)

**Salutation (0–5 points)**

No salutation: 0

Normal: “Hi”, “Hello”: 2

Good: “Good Morning”, “Hello everyone”: 4

Excellent: Includes phrases like “I am excited to introduce”: 5

Keyword Presence (30 points)

Mandatory keywords (4 points each):

Name, Age, School/Class, Family, Hobbies/Interest

Good-to-have keywords (2 points each):

Origin, Ambition/Goal, Fun fact/Unique, Strengths/Achievements

Flow (5 points)

Correct order: Salutation → Basic Details → Additional Details → Closing

2. Speech Rate (10 points)

**Measured as words per minute (WPM):**

111–140 WPM: 10 points

141–160 WPM: 6 points

160 WPM: 2 points

81–110 WPM: 6 points

<80 WPM: 2 points

3. Language & Grammar (20 points)

**Grammar Errors (10 points) using language-tool-python:**

0.9 errors/100 words: 10

0.7–0.89: 8

0.5–0.69: 6

0.3–0.49: 4

<0.3: 2

**Vocabulary Richness (TTR) (10 points)**

**TTR = distinct words ÷ total words**

0.9–1.0: 10

0.7–0.89: 8

0.5–0.69: 6

0.3–0.49: 4

0–0.29: 2

4. Clarity (15 points)

**Filler Word Rate (um, uh, like, you know…):**

0–3%: 15

4–6%: 12

7–9%: 9

10–12%: 6

≥13%: 3

5. Engagement (15 points)

**Sentiment / Positivity using VADER:**

≥0.9: 15

0.7–0.89: 12

0.5–0.69: 9

0.3–0.49: 6

<0.3: 3

---

## EXAMPLE

**Input**
Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family...

**Output**
{
  "salutation": 4,
  "keywords": 24,
  "keywords_detail": {
    "must": ["name", "age", "class_school", "family", "hobby"],
    "good": ["fun_fact", "unique"]
  },
  "flow": 5,
  "wpm": 10,
  "grammar": 8,
  "vocab": 6,
  "filler": 15,
  "sentiment": 3,
  "overall": 70
}

---


## Notes

The scoring is dynamic and proportional based on the rubric.

You can adjust weights or thresholds in app.py to tune the evaluation.

Supports future NLP enhancements like semantic similarity scoring via **sentence-transformers**.

---

## Prototype Link:




