# ==============================================================
# pages/1_Message_Analyzer.py
# Page 1 — Paste a suspicious message and get instant analysis
#
# v5 additions:
#   - English / Spanish interface via utils/translations.py
#   - Read Aloud + Stop Speaking using browser Web Speech API
#     injected through st.components.v1.html()
#   - Language selector carried from Home.py via session state
# ==============================================================

import streamlit as st
import streamlit.components.v1 as components
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.scam_detector import analyze_message
from utils.translations import T

st.set_page_config(
    page_title="Message Analyzer — ShieldFromScamApp",
    page_icon="📩",
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

# ── Language (set by Home.py sidebar; default to English) ────────────────────
lang = st.session_state.get("lang", "en")

# ── Language selector also shown in this page's sidebar ──────────────────────
# This mirrors the Home.py selector so the user can switch language
# without going back to the home page.
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

st.sidebar.title("🛡️ ShieldFromScamApp")
st.sidebar.markdown("---")
lang_choice = st.sidebar.radio(
    T("en", "lang_label"),
    options=["English", "Español"],
    index=0 if st.session_state["lang"] == "en" else 1,
    key="lang_radio_analyzer",
)
st.session_state["lang"] = "en" if lang_choice == "English" else "es"
lang = st.session_state["lang"]

# ── Session state defaults ────────────────────────────────────────────────────
if "show_result" not in st.session_state:
    st.session_state["show_result"] = False
if "clear_count" not in st.session_state:
    st.session_state["clear_count"] = 0

# ── Page header ───────────────────────────────────────────────────────────────
st.title(T(lang, "analyzer_title"))
st.markdown(T(lang, "analyzer_intro"))
st.info(T(lang, "analyzer_lang_note"))
st.markdown("---")

# ── Example messages ──────────────────────────────────────────────────────────
with st.expander(T(lang, "example_label")):
    example_labels = [
        T(lang, "example_none"),
        T(lang, "example_irs"),
        T(lang, "example_lottery"),
        T(lang, "example_tech"),
        T(lang, "example_gift"),
    ]
    example_choice = st.radio(
        T(lang, "example_choose"),
        example_labels,
        horizontal=True,
        key="example_radio",
    )

# Examples are always in English so the detector sees the original language
EXAMPLES = {
    T(lang, "example_irs"): (
        "URGENT: This is the IRS. Your Social Security Number has been suspended "
        "due to suspicious activity. You must call back immediately at 1-800-555-0199 "
        "or a warrant will be issued for your arrest."
    ),
    T(lang, "example_lottery"): (
        "Congratulations you have won $1,000,000 in the National Lottery. "
        "To claim your prize, please send a processing fee of $500 via Western Union "
        "and provide your bank account number and routing number."
    ),
    T(lang, "example_tech"): (
        "WARNING: Your computer is infected with a dangerous virus! "
        "Call Apple Support immediately at 1-888-555-0177. "
        "Allow our technician remote access to remove the virus before your data is deleted."
    ),
    T(lang, "example_gift"): (
        "Hi, this is your Amazon account team. Your account has been suspended. "
        "To verify your account and restore access, purchase $200 in Amazon gift cards "
        "and reply with the codes. Act now — your account expires today!"
    ),
}

# ── Text area ─────────────────────────────────────────────────────────────────
textarea_key = f"msg_input_{st.session_state['clear_count']}"
prefill = EXAMPLES.get(example_choice, "")

user_message = st.text_area(
    T(lang, "textarea_label"),
    value=prefill,
    height=200,
    placeholder=T(lang, "textarea_placeholder"),
    key=textarea_key,
)

# ── Analyze / Clear buttons ───────────────────────────────────────────────────
col1, col2 = st.columns([1, 3])
with col1:
    analyze_clicked = st.button(T(lang, "btn_analyze"), use_container_width=True)
with col2:
    clear_clicked = st.button(T(lang, "btn_clear"), use_container_width=True)

if clear_clicked:
    st.session_state["clear_count"] += 1
    st.session_state["show_result"] = False
    if "last_result" in st.session_state:
        del st.session_state["last_result"]
    st.rerun()

st.markdown("---")

# ── Run analysis ──────────────────────────────────────────────────────────────
if analyze_clicked:
    if not user_message.strip():
        st.warning(T(lang, "warn_empty"))
    else:
        result = analyze_message(user_message)
        st.session_state["show_result"] = True
        st.session_state["last_result"] = result

# ── Display result ────────────────────────────────────────────────────────────
if st.session_state.get("show_result") and "last_result" in st.session_state:
    result = st.session_state["last_result"]
    score  = result["score"]

    # ── Translate verdict string ──────────────────────────────
    raw_verdict = result["verdict"]   # English from analyze_message()
    if "Looks Safe" in raw_verdict:
        display_verdict = T(lang, "verdict_safe")
        advice_key      = "advice_safe"
    elif "Slightly Suspicious" in raw_verdict:
        display_verdict = T(lang, "verdict_slightly")
        advice_key      = "advice_slightly"
    elif "Suspicious" in raw_verdict:
        display_verdict = T(lang, "verdict_suspicious")
        advice_key      = "advice_suspicious"
    else:
        display_verdict = T(lang, "verdict_scam")
        advice_key      = "advice_scam"

    # ── Risk score bar ────────────────────────────────────────
    st.subheader(T(lang, "results_score_header"))

    if score < 15:
        bar_color = "#28a745"
    elif score < 35:
        bar_color = "#17a2b8"
    elif score < 60:
        bar_color = "#ffc107"
    else:
        bar_color = "#dc3545"

    st.markdown(
        f"""
        <div style="background:#e9ecef;border-radius:8px;height:28px;width:100%;margin-bottom:6px;">
          <div style="background:{bar_color};width:{score}%;height:28px;border-radius:8px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"**{T(lang, 'results_score_of', score=score)}**")

    # ── Verdict ───────────────────────────────────────────────
    st.markdown(f"### {T(lang, 'results_verdict_header')}")
    if result["color"] == "success":
        st.success(display_verdict)
    elif result["color"] == "info":
        st.info(display_verdict)
    elif result["color"] == "warning":
        st.warning(display_verdict)
    else:
        st.error(display_verdict)

    # ── Warning signs ─────────────────────────────────────────
    st.markdown(f"### {T(lang, 'results_warnings_header')}")
    if result["reasons"]:
        for reason in result["reasons"]:
            st.markdown(f"- {reason}")
    else:
        st.info(T(lang, "results_no_warnings"))

    # ── Safety advice ─────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### {T(lang, 'results_action_header')}")
    st.markdown(T(lang, advice_key))

    # ── Read Aloud section ────────────────────────────────────
    st.markdown("---")

    # Build the text the browser will read aloud.
    # We concatenate score, verdict, each warning sign (emoji-stripped for
    # cleaner speech), and the safety advice.
    def _strip_emoji_markdown(text: str) -> str:
        """Remove markdown bold markers and common emoji for cleaner TTS."""
        import re
        text = re.sub(r"\*\*", "", text)          # remove **bold**
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # [text](url) → text
        # Remove common emoji by stripping non-ASCII + a narrow set
        text = re.sub(r"[^\x00-\x7F🚩]", "", text)
        text = text.replace("🚩", "Warning:")
        return text.strip()

    warning_lines = [_strip_emoji_markdown(r) for r in result["reasons"]]
    warnings_text = (
        ". ".join(warning_lines)
        if warning_lines
        else (
            "No known scam phrases detected."
            if lang == "en"
            else "No se detectaron frases de estafa conocidas."
        )
    )

    advice_plain = _strip_emoji_markdown(T(lang, advice_key))
    # Convert markdown list dashes to readable sentences
    advice_plain = advice_plain.replace("\n- ", ". ").lstrip("- ")

    score_phrase = (
        f"Risk score: {score} out of 100. Verdict: {display_verdict}."
        if lang == "en"
        else f"Puntuación de riesgo: {score} de 100. Veredicto: {display_verdict}."
    )
    warnings_label = "Warning signs found:" if lang == "en" else "Señales de alerta encontradas:"
    advice_label   = "What you should do:" if lang == "en" else "Qué debes hacer:"

    full_speech_text = (
        f"{score_phrase} "
        f"{warnings_label} {warnings_text}. "
        f"{advice_label} {advice_plain}"
    )

    # BCP-47 language tag for Web Speech API voice selection
    speech_lang = "en-US" if lang == "en" else "es-US"

    # Escape for safe embedding in a JS string (handles quotes/newlines)
    def _js_escape(s: str) -> str:
        return (
            s.replace("\\", "\\\\")
             .replace("`", "\\`")
             .replace("$", "\\$")
        )

    speech_js_text = _js_escape(full_speech_text)

    read_label = T(lang, "btn_read_aloud")
    stop_label = T(lang, "btn_stop_speaking")
    unsupported_msg = T(lang, "read_aloud_unsupported")

    # ── Inject the Read Aloud component ──────────────────────────────────────
    # We use st.components.v1.html() which renders inside an <iframe>.
    # The iframe DOES have access to window.speechSynthesis in Chrome and Edge.
    # Height is set to exactly fit the two buttons.
    read_aloud_html = f"""
    <div style="font-family:sans-serif;">
      <button id="readBtn"
        onclick="startSpeech()"
        style="
          font-size:18px; padding:0.5em 1.2em; margin-right:10px;
          border-radius:8px; border:none; cursor:pointer;
          background-color:#1a3c6e; color:white;">
        {read_label}
      </button>
      <button id="stopBtn"
        onclick="stopSpeech()"
        style="
          font-size:18px; padding:0.5em 1.2em;
          border-radius:8px; border:none; cursor:pointer;
          background-color:#6c757d; color:white;">
        {stop_label}
      </button>
      <p id="statusMsg" style="margin-top:10px; color:#555; font-size:15px;"></p>
    </div>

    <script>
      var speechText  = `{speech_js_text}`;
      var speechLang  = "{speech_lang}";
      var statusEl    = document.getElementById("statusMsg");

      function startSpeech() {{
        if (!("speechSynthesis" in window)) {{
          statusEl.textContent = "{_js_escape(unsupported_msg)}";
          statusEl.style.color = "#dc3545";
          return;
        }}
        // Cancel any ongoing speech first
        window.speechSynthesis.cancel();

        var utter = new SpeechSynthesisUtterance(speechText);
        utter.lang = speechLang;
        utter.rate = 0.92;   // slightly slower — easier to understand

        // Try to find a voice in the requested language
        var voices = window.speechSynthesis.getVoices();
        var match  = voices.find(function(v) {{
          return v.lang.startsWith(speechLang.split("-")[0]);
        }});
        if (match) {{ utter.voice = match; }}

        utter.onstart = function() {{
          statusEl.textContent = "{('Speaking...' if lang == 'en' else 'Hablando...')}";
          statusEl.style.color = "#28a745";
        }};
        utter.onend = function() {{
          statusEl.textContent = "{('Done.' if lang == 'en' else 'Listo.')}";
          statusEl.style.color = "#555";
        }};
        utter.onerror = function(e) {{
          statusEl.textContent = "Speech error: " + e.error;
          statusEl.style.color = "#dc3545";
        }};

        window.speechSynthesis.speak(utter);
      }}

      function stopSpeech() {{
        if ("speechSynthesis" in window) {{
          window.speechSynthesis.cancel();
          statusEl.textContent = "{('Stopped.' if lang == 'en' else 'Detenido.')}";
          statusEl.style.color = "#555";
        }}
      }}

      // Chrome requires voices to be loaded before they can be matched.
      // This fires the voice list load so the language match works.
      if ("speechSynthesis" in window) {{
        window.speechSynthesis.getVoices();
        window.speechSynthesis.addEventListener("voiceschanged", function() {{
          window.speechSynthesis.getVoices(); // refresh the list
        }});
      }}
    </script>
    """

    components.html(read_aloud_html, height=120)
