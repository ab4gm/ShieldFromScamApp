# ==============================================================
# pages/3_Scam_Library.py
# Page 3 — Educational reference on common scam types
# v5: Language selector added; page header translated.
#     Scam content shown in English (educational detail preserved).
# ==============================================================

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.translations import T

st.set_page_config(
    page_title="Scam Library — ShieldFromScamApp",
    page_icon="📚",
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
    key="lang_radio_library",
)
st.session_state["lang"] = "en" if lang_choice == "English" else "es"
lang = st.session_state["lang"]

# ── Translated labels ─────────────────────────────────────────────────────────
_ui = {
    "title": {
        "en": "📚 Scam Library",
        "es": "📚 Biblioteca de Estafas",
    },
    "intro": {
        "en": "Learn about the most common scam types, how they work, and how to protect yourself. Click on any scam type to expand it.",
        "es": "Aprende sobre los tipos de estafas más comunes, cómo funcionan y cómo protegerte. Haz clic en cualquier tipo de estafa para expandirlo.",
    },
    "how": {"en": "**How it works:**",         "es": "**Cómo funciona:**"},
    "signs": {"en": "**⚠️ Warning signs:**",   "es": "**⚠️ Señales de alerta:**"},
    "protect": {"en": "**🛡️ How to protect yourself:**", "es": "**🛡️ Cómo protegerte:**"},
    "tip": {
        "en": "💡 **Golden Rule:** If something feels off — slow down, verify independently, and talk to someone you trust before taking any action.",
        "es": "💡 **Regla de oro:** Si algo no se siente bien — tómate tu tiempo, verifica por tu cuenta y habla con alguien de confianza antes de actuar.",
    },
}

def ui(key):
    return _ui[key].get(lang) or _ui[key]["en"]

st.title(ui("title"))
st.markdown(ui("intro"))
st.markdown("---")

scams = [
    {
        "title": "📞 Phone & Robocall Scams",
        "how": "Scammers call you pretending to be the IRS, Social Security, Medicare, a bank, or even a family member in trouble. They create urgency (you owe taxes, your number was suspended, you'll be arrested) to get you to act fast.",
        "signs": ["Threats of arrest or legal action", "Demands for immediate payment via gift card, wire transfer, or crypto", "Caller ID that looks like a government number (fake — called 'spoofing')", "Robotic pre-recorded voice"],
        "protect": ["Hang up immediately — government agencies contact you by mail first", "Never call back numbers from suspicious calls", "Use a spam-call blocker app (e.g., Hiya, Nomorobo)"],
    },
    {
        "title": "📧 Email Phishing Scams",
        "how": "A fake email impersonates a trusted company (Amazon, PayPal, your bank) and tricks you into clicking a fake link or downloading a malicious file. The goal is to steal your password, credit card, or personal info.",
        "signs": ["Sender email doesn't match the real company (e.g., amazon-support99@gmail.com)", "Urgent subject lines: 'Your account will be deleted!'", "Links that look real but go somewhere else (hover to check!)", "Poor spelling and grammar"],
        "protect": ["Never click links in emails — go directly to the website instead", "Check the sender's full email address (not just the display name)", "Enable two-factor authentication on all accounts"],
    },
    {
        "title": "📱 Text Message (Smishing) Scams",
        "how": "Scam texts (called 'smishing') pretend to be package delivery notices, bank alerts, or prize notifications. They contain links that lead to fake websites designed to steal your information.",
        "signs": ["Unexpected package delivery messages with a link", "Texts from unknown numbers claiming to be your bank", "Prize or gift card winning notifications", "Shortened or strange-looking links"],
        "protect": ["Don't click links in texts from unknown numbers", "Track packages directly on the shipper's official website", "Report smishing to 7726 (SPAM) — works on most US carriers"],
    },
    {
        "title": "🏆 Lottery & Prize Scams",
        "how": "You're told you've won a lottery, sweepstakes, or prize — but you never entered. To 'claim' your prize, you must pay taxes, fees, or shipping costs upfront. Of course, there is no prize.",
        "signs": ["You won something you never entered", "Must pay fees upfront to receive your prize", "Prize amount is unrealistically large", "Requests for personal information to 'verify' your identity"],
        "protect": ["Remember: If you didn't enter, you can't win", "Legitimate prizes never require upfront payment", "Never give personal or financial information to claim a prize"],
    },
    {
        "title": "❤️ Romance Scams",
        "how": "A scammer creates a fake profile on a dating site or social media and builds a relationship with you over weeks or months. Once they've earned your trust, they ask for money — often claiming an emergency, medical need, or travel problem.",
        "signs": ["They're extremely attractive and their profile photos look 'too perfect'", "They fall in love very quickly", "They always have an excuse not to video chat", "They ask for gift cards, wire transfers, or crypto"],
        "protect": ["Reverse image search their profile photo (Google Images)", "Never send money to someone you haven't met in person", "Talk to a trusted friend or family member about the relationship"],
    },
    {
        "title": "💻 Tech Support Scams",
        "how": "A pop-up or phone call claims your computer has a virus. You're told to call a 'support' number or allow remote access. The scammer then either charges you for fake 'fixes' or installs real malware on your device.",
        "signs": ["Scary pop-ups saying your computer is infected", "Unsolicited calls claiming to be from Microsoft or Apple", "Requests to download remote access software (AnyDesk, TeamViewer)", "Demands for payment to 'fix' a problem you didn't know you had"],
        "protect": ["Real tech companies don't call you out of the blue", "Close scary pop-ups — they're fake (press Alt+F4 or force-quit)", "Never give anyone remote access to your computer unless YOU initiated the call"],
    },
    {
        "title": "🏠 Grandparent / Family Emergency Scams",
        "how": "A scammer calls pretending to be your grandchild (or another family member) in trouble — arrested, in an accident, or stranded. They ask you to wire money secretly and not tell other family members.",
        "signs": ["Unexpected call saying a family member is in danger", "Caller says 'Please don't tell Mom and Dad'", "Asks for immediate cash, gift cards, or wire transfer", "A 'lawyer' or 'police officer' also gets on the phone"],
        "protect": ["Hang up and call your family member directly on their known number", "Set up a family 'code word' for real emergencies", "Never send money based on a single unexpected call"],
    },
    {
        "title": "💰 Investment & Crypto Scams",
        "how": "Scammers promise guaranteed high returns on investments, often in cryptocurrency. They may show you fake dashboards with growing balances. When you try to withdraw, they demand more fees and then disappear.",
        "signs": ["Guaranteed profits with no risk", "Someone you met online is pushing a specific investment", "High-pressure tactics to invest quickly", "You can see 'profits' but can't withdraw them"],
        "protect": ["No legitimate investment guarantees returns", "Research any investment on the SEC website: investor.gov", "Be extremely skeptical of crypto investment advice from online contacts"],
    },
]

for scam in scams:
    with st.expander(scam["title"]):
        st.markdown(ui("how"))
        st.markdown(scam["how"])
        st.markdown(ui("signs"))
        for sign in scam["signs"]:
            st.markdown(f"- {sign}")
        st.markdown(ui("protect"))
        for tip in scam["protect"]:
            st.markdown(f"- {tip}")

st.markdown("---")
st.info(ui("tip"))
