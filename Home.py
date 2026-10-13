# ==============================================================
# ShieldFromScamApp — Main Entry Point
# Congressional App Challenge, District 6
# ==============================================================
# This is the first file Streamlit runs.
# It sets up the page layout and shows the Home screen.
# ==============================================================

import streamlit as st
import sys
import os

# Make utils importable from every page
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.translations import T

# ── Page configuration (must be the VERY first Streamlit call) ──
st.set_page_config(
    page_title="ShieldFromScamApp",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS: larger text and friendly colors ──
st.markdown(
    """
    <style>
        html, body, [class*="css"] { font-size: 18px !important; }
        h1 { color: #1a3c6e; }
        .stButton > button {
            font-size: 18px !important;
            padding: 0.6em 1.4em !important;
            border-radius: 8px !important;
            background-color: #1a3c6e !important;
            color: white !important;
        }
        .stButton > button:hover { background-color: #2e5fa3 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Language selector (sidebar — persists across all pages) ──────────────────
# Initialize language in session state on first load
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

st.sidebar.title("🛡️ ShieldFromScamApp")
st.sidebar.markdown("---")

# Language radio — changing it immediately updates session state
lang_choice = st.sidebar.radio(
    T("en", "lang_label"),          # always show label in both languages
    options=["English", "Español"],
    index=0 if st.session_state["lang"] == "en" else 1,
    key="lang_radio",
)
st.session_state["lang"] = "en" if lang_choice == "English" else "es"
lang = st.session_state["lang"]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{T(lang, 'nav_label')}**")
st.sidebar.info(T(lang, "nav_hint"))

# ── Home page content ─────────────────────────────────────────────────────────
st.title(T(lang, "home_title"))
st.subheader(T(lang, "home_subtitle"))
st.markdown("---")

st.markdown(f"### {T(lang, 'home_welcome')}")
st.markdown(T(lang, "home_intro"))
st.markdown("---")

st.markdown(f"### {T(lang, 'home_features_header')}")
st.markdown(T(lang, "home_table"))
st.markdown("---")

st.markdown(f"### {T(lang, 'home_howto_header')}")
st.markdown(T(lang, "home_howto"))
st.markdown("---")

st.success(T(lang, "home_tip"))
