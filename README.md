# SpeechAI

# Speech Scoring 

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



---

##  Scoring Rubric

SpeechAI uses **three layers of analysis**:

### **1️⃣ Rule-Based Processing**
Uses regex and pattern matching for:
- Salutation  
- Keyword scoring (mandatory + good-to-have)  
- Flow and order  
- Filler word detection  
- Word & sentence counts  
- WPM scoring  

---

### **2️⃣ NLP-Based Processing**
Uses natural language tools for deeper quality analysis:
- **LanguageTool** → grammar error detection  
- **VADER** → sentiment & engagement scoring  

---

### **3️⃣ Weighted Score Aggregation**
Scores are normalized and combined:

| Criterion | Weight |
|----------|--------|
| Content & Structure | 40 |
| Speech Rate (WPM) | 10 |
| Grammar | 10 |
| Vocabulary (TTR) | 10 |
| Clarity (Filler words) | 15 |
| Engagement (Sentiment) | 15 |
| **Total** | **100** |

Results are returned as a JSON breakdown + total score.

---

## 📊 Scoring Rubric (Detailed)

### **1. Content & Structure (40 points)**

#### **Salutation (0–5)**
- No salutation → 0  
- “Hi”, “Hello” → 2  
- “Good morning”, “Hello everyone” → 4  
- “I am excited to introduce…” → 5  

#### **Keyword Presence (30)**
**Mandatory keywords** (4 points each):
- Name  
- Age  
- School/Class  
- Family  
- Hobby  

**Good-to-have keywords** (2 points each):
- Origin  
- Goal/Ambition  
- Fun Fact / Unique Trait  
- Achievement  

#### **Flow (5)**
Correct order:
**Salutation → Basic Details → Additional Details → Closing**

---

### **2. Speech Rate (WPM) — 10 points**

| WPM Range | Points |
|-----------|--------|
| 111–140 | 10 |
| 141–160 | 6 |
| >160 | 2 |
| 81–110 | 6 |
| <80 | 2 |

---

### **3. Grammar — 10 points**

Based on **LanguageTool error rate per 100 words**.

---

### **4. Vocabulary (TTR) — 10 points**

TTR = unique words ÷ total words  
Higher TTR → richer vocabulary.

---

### **5. Clarity (Filler Words) — 15 points**

Detects fillers: *um, uh, like, you know, actually, basically…*

Lower percentage → higher score.

---

### **6. Engagement (Sentiment) — 15 points**

Based on VADER positivity score.

---


## EXAMPLE

**Input**
Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family...


### **Output**
```json
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
```

## Local Installations

1. Create Virtual Environment

python -m venv venv

venv\Scripts\activate   # Windows

2. Install dependencies

pip install -r requirements.txt

3. Run the app
python app.py

Connect to JRE>=17

---

## Notes

**Deployment Limitation**

The current version of the project uses LanguageTool for grammar analysis, which requires a local Java Runtime Environment (JRE). This significantly increases the memory footprint during build and runtime.

At this time, I am unable to subscribe to paid hosting services, so deployment is not feasible. The backend logic, scoring system, and UI are fully functional; only hosting is restricted due to resource limitations.


---




