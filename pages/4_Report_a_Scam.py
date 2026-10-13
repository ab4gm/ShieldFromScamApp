# ==============================================================
# pages/4_Report_a_Scam.py
# Page 4 — Where and how to report scams in the US
# v5: Language selector added; page header and labels translated.
# ==============================================================

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.translations import T

st.set_page_config(
    page_title="Report a Scam — ShieldFromScamApp",
    page_icon="📞",
    layout="centered",
)

st.markdown(
    """
    <style>
        html, body, [class*="css"] { font-size: 18px !important; }
        h1 { color: #1a3c6e; }
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
    key="lang_radio_report",
)
st.session_state["lang"] = "en" if lang_choice == "English" else "es"
lang = st.session_state["lang"]

# ── Translated labels ─────────────────────────────────────────────────────────
_ui = {
    "title":    {"en": "📞 Report a Scam",       "es": "📞 Reportar una Estafa"},
    "intro":    {
        "en": "**Reporting scams helps protect everyone.** Here's exactly where to report different types of scams in the United States.",
        "es": "**Reportar estafas ayuda a proteger a todos.** Aquí encontrarás exactamente dónde reportar diferentes tipos de estafas en los Estados Unidos.",
    },
    "alert":    {
        "en": "🚨 **If you've already lost money or given personal information to a scammer, contact your bank immediately and consider placing a fraud alert with the credit bureaus.**",
        "es": "🚨 **Si ya perdiste dinero o diste información personal a un estafador, contacta a tu banco de inmediato y considera colocar una alerta de fraude con las agencias de crédito.**",
    },
    "best_for": {"en": "**Best for:**",           "es": "**Mejor para:**"},
    "website":  {"en": "🌐 **Website:**",         "es": "🌐 **Sitio web:**"},
    "phone":    {"en": "📞 **Phone:**",            "es": "📞 **Teléfono:**"},
    "texts_title": {
        "en": "📱 Reporting Scam Texts",
        "es": "📱 Cómo Reportar Textos de Estafa",
    },
    "texts_body": {
        "en": "Forward suspicious text messages to **7726 (SPAM)** — this works on most US carriers including Verizon, AT&T, and T-Mobile. It's free and helps your carrier block spam numbers.",
        "es": "Reenvía mensajes de texto sospechosos al **7726 (SPAM)** — funciona en la mayoría de los operadores de EE.UU. incluyendo Verizon, AT&T y T-Mobile. Es gratis y ayuda a tu operador a bloquear números de spam.",
    },
    "freeze_title": {
        "en": "🛑 Place a Fraud Alert or Credit Freeze",
        "es": "🛑 Colocar una Alerta de Fraude o Congelamiento de Crédito",
    },
    "freeze_body": {
        "en": "If your personal information was stolen, contact the three major credit bureaus:",
        "es": "Si tu información personal fue robada, contacta a las tres principales agencias de crédito:",
    },
    "visit": {"en": "Visit Site", "es": "Visitar Sitio"},
    "footer": {
        "en": "💬 **Remember:** Reporting scams might not get your money back, but it helps authorities catch scammers and protect other people.",
        "es": "💬 **Recuerda:** Reportar estafas puede no recuperar tu dinero, pero ayuda a las autoridades a atrapar estafadores y proteger a otras personas.",
    },
}

def ui(key):
    return _ui[key].get(lang) or _ui[key]["en"]

st.title(ui("title"))
st.markdown(ui("intro"))
st.markdown("---")
st.error(ui("alert"))
st.markdown("---")

resources = [
    {"org": "🏛️ Federal Trade Commission (FTC)", "for": "Most scams — the #1 place to report fraud in the USA", "url": "https://reportfraud.ftc.gov", "phone": "1-877-FTC-HELP (1-877-382-4357)"},
    {"org": "🌐 FBI Internet Crime Complaint Center (IC3)", "for": "Online scams, phishing, cyber fraud, romance scams", "url": "https://www.ic3.gov", "phone": None},
    {"org": "📱 Federal Communications Commission (FCC)", "for": "Robocalls, phone scams, smishing texts", "url": "https://consumercomplaints.fcc.gov", "phone": "1-888-CALL-FCC (1-888-225-5322)"},
    {"org": "👴 AARP Fraud Watch Network", "for": "Scams targeting seniors — free helpline staffed by volunteers", "url": "https://www.aarp.org/money/scams-fraud/", "phone": "1-877-908-3360"},
    {"org": "💰 Consumer Financial Protection Bureau (CFPB)", "for": "Financial scams, bank fraud, debt collector scams", "url": "https://www.consumerfinance.gov/complaint/", "phone": "1-855-411-CFPB (1-855-411-2372)"},
    {"org": "📬 US Postal Inspection Service", "for": "Mail fraud, sweepstakes by mail, fake checks by mail", "url": "https://postalinspectors.uspis.gov/", "phone": "1-877-876-2455"},
    {"org": "🔐 Identity Theft — IdentityTheft.gov", "for": "If your personal information or identity was stolen", "url": "https://www.identitytheft.gov", "phone": "1-877-ID-THEFT (1-877-438-4338)"},
]

for r in resources:
    with st.container():
        st.markdown(f"### {r['org']}")
        st.markdown(f"{ui('best_for')} {r['for']}")
        st.markdown(f"{ui('website')} [{r['url']}]({r['url']})")
        if r["phone"]:
            st.markdown(f"{ui('phone')} {r['phone']}")
        st.markdown("---")

st.subheader(ui("texts_title"))
st.markdown(ui("texts_body"))
st.markdown("---")

st.subheader(ui("freeze_title"))
st.markdown(ui("freeze_body"))

bureaus = [
    ("Equifax",    "https://www.equifax.com/personal/credit-report-services/credit-fraud-alerts/", "1-800-685-1111"),
    ("Experian",   "https://www.experian.com/fraud/center.html",                                   "1-888-397-3742"),
    ("TransUnion", "https://www.transunion.com/fraud-alerts",                                      "1-800-916-8800"),
]

cols = st.columns(3)
for col, (name, url, phone) in zip(cols, bureaus):
    with col:
        st.markdown(f"**{name}**")
        st.markdown(f"[{ui('visit')}]({url})")
        st.markdown(f"📞 {phone}")

st.markdown("---")
st.success(ui("footer"))
