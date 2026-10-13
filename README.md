# 🛡️ ShieldFromScamApp

**A free, beginner-friendly scam detection app — 2026 Congressional App Challenge, District 6**

ShieldFromScamApp helps everyday people — especially seniors and those less familiar with technology — identify potential scams in text messages, emails, and other written communications.

---

## 🔍 What It Does

Paste any suspicious message into the **Message Analyzer** and get back:

- A **risk score** from 0 to 100
- A **verdict**: Looks Safe / Slightly Suspicious / Suspicious / Likely a Scam
- A clear explanation of **every warning sign** detected and why it matters
- **Safety recommendations** for what to do next
- A **Read Aloud** button that reads the results out loud (no API needed)
- Full **English / Spanish** interface

---

## 📋 Features

| Page | Description |
|---|---|
| 📩 Message Analyzer | Paste any suspicious text, email, or call script for instant analysis |
| 🧠 Scam Quiz | 8-question interactive quiz to sharpen your scam-spotting skills |
| 📚 Scam Library | Plain-language guides to 8 major scam types |
| 📞 Report a Scam | Direct links and phone numbers to all major US fraud reporting agencies |
| ℹ️ About | How the app works and its limitations |

---

## 🚀 How to Run Locally

**Requirements:** Python 3.12, pip

```bash
# 1. Clone this repository
git clone https://github.com/YOUR_USERNAME/ShieldFromScamApp.git
cd ShieldFromScamApp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run Home.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 🌐 Live App

Deployed on Streamlit Community Cloud:  
👉 **[YOUR_STREAMLIT_URL_HERE]**

---

## 🛠️ Built With

- **Python 3.12**
- **Streamlit 1.38.0**
- **Browser Web Speech API** — powers Read Aloud (no paid API needed)
- No external APIs or paid services — runs entirely on the user's device

---

## ⚠️ Limitations

- Detection uses pattern matching, not AI. A low score does not guarantee a message is safe.
- Works best with English-language messages. Spanish interface is available.
- Results are not legal or financial advice. Always verify independently.

---

## 📄 License

Created for the 2026 Congressional App Challenge. Educational and non-commercial use.
