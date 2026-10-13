# ==============================================================
# pages/2_Scam_Quiz.py
# Page 2 — Interactive quiz to test scam-spotting skills
# v5: Language selector added (sidebar) — quiz content in English
#     with translated UI labels (buttons, score, instructions).
# ==============================================================

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.translations import T

st.set_page_config(
    page_title="Scam Quiz — ShieldFromScamApp",
    page_icon="🧠",
    layout="centered",
)

st.markdown(
    """
    <style>
        html, body, [class*="css"] { font-size: 18px !important; }
        h1 { color: #1a3c6e; }
        .stButton > button {
            font-size: 18px !important; padding: 0.6em 1.4em !important;
            border-radius: 8px !important;
            background-color: #1a3c6e !important; color: white !important;
        }
        .stButton > button:hover { background-color: #2e5fa3 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Language selector ─────────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

st.sidebar.title("🛡️ ShieldFromScamApp")
st.sidebar.markdown("---")
lang_choice = st.sidebar.radio(
    T("en", "lang_label"),
    options=["English", "Español"],
    index=0 if st.session_state["lang"] == "en" else 1,
    key="lang_radio_quiz",
)
st.session_state["lang"] = "en" if lang_choice == "English" else "es"
lang = st.session_state["lang"]

# ── Translated UI labels ──────────────────────────────────────────────────────
_ui = {
    "title":       {"en": "🧠 Scam Spotter Quiz",     "es": "🧠 Quiz Detecta-Estafas"},
    "intro":       {"en": "Read each scenario and decide: **Scam or Legit?**  \nSee how well you can spot the tricks scammers use!",
                    "es": "Lee cada situación y decide: **¿Estafa o Legítimo?**  \n¡Descubre qué tan bien puedes detectar los trucos de los estafadores!"},
    "question_of": {"en": "Question {i} of {n}",      "es": "Pregunta {i} de {n}"},
    "scenario":    {"en": "📋 Scenario:",              "es": "📋 Situación:"},
    "is_scam":     {"en": "**Is this a scam or legit?**", "es": "**¿Es una estafa o es legítimo?**"},
    "btn_scam":    {"en": "🚩 SCAM",                   "es": "🚩 ESTAFA"},
    "btn_legit":   {"en": "✅ LEGIT",                  "es": "✅ LEGÍTIMO"},
    "correct":     {"en": "✅ Correct!",               "es": "✅ ¡Correcto!"},
    "wrong":       {"en": "❌ Not quite.",             "es": "❌ No del todo."},
    "explanation": {"en": "#### 💡 Explanation:",      "es": "#### 💡 Explicación:"},
    "next_q":      {"en": "➡️ Next Question",          "es": "➡️ Siguiente Pregunta"},
    "see_results": {"en": "🏁 See My Results",         "es": "🏁 Ver Mis Resultados"},
    "quiz_done":   {"en": "## 🎉 Quiz Complete!",      "es": "## 🎉 ¡Quiz Completado!"},
    "score_label": {"en": "### Your Score: **{score} / {total}** ({pct}%)",
                    "es": "### Tu Puntuación: **{score} / {total}** ({pct}%)"},
    "perfect":     {"en": "🏆 Perfect score! You're a scam-spotting expert!",
                    "es": "🏆 ¡Puntaje perfecto! ¡Eres un experto detectando estafas!"},
    "great":       {"en": "🛡️ Great job! You have strong scam awareness.",
                    "es": "🛡️ ¡Muy bien! Tienes una sólida conciencia sobre estafas."},
    "ok":          {"en": "⚠️ Not bad, but keep learning — scammers can be tricky!",
                    "es": "⚠️ No está mal, ¡pero sigue aprendiendo — los estafadores pueden ser astutos!"},
    "risk":        {"en": "🚨 You may be at risk. Review the Scam Library to learn more.",
                    "es": "🚨 Puedes estar en riesgo. Revisa la Biblioteca de Estafas para aprender más."},
    "restart":     {"en": "🔄 Restart Quiz",           "es": "🔄 Reiniciar Quiz"},
}

def ui(key, **kw):
    text = _ui[key].get(lang) or _ui[key]["en"]
    return text.format(**kw) if kw else text

# ── Quiz data (scenarios always in English for authenticity) ──────────────────
QUESTIONS = [
    {
        "scenario": "📱 You get a text message: 'Your package could not be delivered. Pay a $3.99 redelivery fee here: bit.ly/track-pkg8812'",
        "answer": True,
        "explanation": "🚩 **Scam!** This is a fake package delivery phishing text. Scammers impersonate USPS, FedEx, or UPS. Legitimate carriers never ask for payment via a random short link. Always go directly to the carrier's official website.",
    },
    {
        "scenario": "📧 You receive an email from your bank saying: 'We noticed unusual activity on your account. Please log in at our secure website www.chasebank.com to review your recent transactions.'",
        "answer": False,
        "explanation": "✅ **Could be Legit** — if the link goes to the bank's real, official domain. Banks do send security alerts. Key tip: hover over the link BEFORE clicking to confirm it goes to the real domain. Never log in via links in emails — instead, type the bank's address directly in your browser.",
    },
    {
        "scenario": "☎️ You get a call: 'This is the Social Security Administration. Your Social Security Number has been compromised in criminal activity. Press 1 to speak to an officer or your account will be suspended.'",
        "answer": True,
        "explanation": "🚩 **Scam!** The SSA will never call you to threaten suspension of your number. This is an impersonation scam. Hang up immediately. The real SSA number is 1-800-772-1213.",
    },
    {
        "scenario": "💬 A Facebook friend messages you: 'Hey! I'm stuck abroad after getting robbed. I just need $300 wired to me — I'll pay you back when I'm home. Please help me!'",
        "answer": True,
        "explanation": "🚩 **Scam!** This is the 'stranded traveler' or 'friend in distress' scam. Scammers hack or clone social media accounts and send this message to all contacts. Always call your friend directly on their phone to verify before sending any money.",
    },
    {
        "scenario": "📧 You get an email from Amazon saying your order #112-3456789 has shipped and includes a tracking number. The email comes from auto-confirm@amazon.com.",
        "answer": False,
        "explanation": "✅ **Likely Legit** — if you actually placed that order and the email domain is exactly amazon.com (not amazon-support.com or similar). Amazon does send shipping confirmations. Always check the exact sender email domain.",
    },
    {
        "scenario": "🎁 A pop-up on a website says: 'Congratulations! You are today's lucky visitor! Click here to claim your FREE iPhone 15. Limited time offer — expires in 5 minutes!'",
        "answer": True,
        "explanation": "🚩 **Scam!** No website randomly gives away iPhones to visitors. These pop-ups try to get you to click malicious links or give personal info. Close the tab immediately.",
    },
    {
        "scenario": "📞 You receive a call from your credit card company asking you to confirm the last 4 digits of your card and your zip code to verify a suspicious charge.",
        "answer": False,
        "explanation": "✅ **Could be Legit** — credit card fraud departments do call customers. But here's the safe rule: hang up and call the number on the BACK of your card. Never give full card numbers, passwords, or CVV codes to an incoming caller.",
    },
    {
        "scenario": "💌 A romantic interest you met online (but never in person) asks you to invest in their cryptocurrency business. They say they've already made $50,000 and can help you do the same.",
        "answer": True,
        "explanation": "🚩 **Scam!** This is a 'pig butchering' romance + crypto scam. Scammers build fake relationships over weeks before pushing fake crypto investments. Victims have lost tens of thousands of dollars. Never invest money based on advice from someone you've only met online.",
    },
]

# ── Session state ─────────────────────────────────────────────────────────────
if "quiz_index"    not in st.session_state: st.session_state.quiz_index    = 0
if "quiz_score"    not in st.session_state: st.session_state.quiz_score    = 0
if "quiz_answered" not in st.session_state: st.session_state.quiz_answered = False
if "quiz_done"     not in st.session_state: st.session_state.quiz_done     = False

st.title(ui("title"))
st.markdown(ui("intro"))
st.markdown("---")

# ── Results screen ────────────────────────────────────────────────────────────
if st.session_state.quiz_done:
    score = st.session_state.quiz_score
    total = len(QUESTIONS)
    pct   = int((score / total) * 100)

    st.markdown(ui("quiz_done"))
    st.markdown(ui("score_label", score=score, total=total, pct=pct))
    st.progress(pct / 100)

    if pct == 100:   st.success(ui("perfect"))
    elif pct >= 75:  st.success(ui("great"))
    elif pct >= 50:  st.warning(ui("ok"))
    else:            st.error(ui("risk"))

    st.markdown("---")
    if st.button(ui("restart")):
        st.session_state.quiz_index    = 0
        st.session_state.quiz_score    = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_done     = False
        st.rerun()

else:
    idx = st.session_state.quiz_index
    q   = QUESTIONS[idx]

    st.markdown(f"**{ui('question_of', i=idx+1, n=len(QUESTIONS))}**")
    st.progress(idx / len(QUESTIONS))
    st.markdown("---")

    st.markdown(f"### {ui('scenario')}")
    st.info(q["scenario"])
    st.markdown(ui("is_scam"))

    if not st.session_state.quiz_answered:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(ui("btn_scam"), use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.user_answer   = True
                st.rerun()
        with col2:
            if st.button(ui("btn_legit"), use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.user_answer   = False
                st.rerun()

    if st.session_state.quiz_answered:
        user_answer = st.session_state.user_answer
        correct     = user_answer == q["answer"]

        if st.session_state.quiz_answered is True:
            if correct:
                st.session_state.quiz_score += 1
            st.session_state.quiz_answered = "scored"

        if correct: st.success(ui("correct"))
        else:       st.error(ui("wrong"))

        st.markdown(ui("explanation"))
        st.markdown(q["explanation"])
        st.markdown("---")

        if idx + 1 < len(QUESTIONS):
            if st.button(ui("next_q"), use_container_width=True):
                st.session_state.quiz_index    += 1
                st.session_state.quiz_answered  = False
                st.rerun()
        else:
            if st.button(ui("see_results"), use_container_width=True):
                st.session_state.quiz_done     = True
                st.session_state.quiz_answered = False
                st.rerun()
