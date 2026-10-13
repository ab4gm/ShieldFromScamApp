# ==============================================================
# utils/translations.py
# All English and Spanish UI strings for ShieldFromScamApp.
#
# Usage:
#   from utils.translations import T
#   lang = st.session_state.get("lang", "en")
#   st.title(T(lang, "home_title"))
# ==============================================================

_STRINGS = {
    # ── Language selector ──────────────────────────────────────
    "lang_label": {
        "en": "🌐 Language / Idioma",
        "es": "🌐 Idioma / Language",
    },
    "lang_en": {"en": "English", "es": "English"},
    "lang_es": {"en": "Español", "es": "Español"},

    # ── Sidebar / navigation ───────────────────────────────────
    "app_name": {"en": "🛡️ ShieldFromScamApp", "es": "🛡️ ShieldFromScamApp"},
    "nav_label": {"en": "Navigate:", "es": "Navegar:"},
    "nav_hint": {
        "en": "Use the **Pages** menu above (▲) or the links below to explore the app.",
        "es": "Usa el menú de **Páginas** arriba (▲) o los enlaces para explorar la app.",
    },

    # ── Home page ──────────────────────────────────────────────
    "home_title": {"en": "🛡️ ShieldFromScamApp", "es": "🛡️ ShieldFromScamApp"},
    "home_subtitle": {
        "en": "Your smart scam protection tool",
        "es": "Tu herramienta inteligente contra estafas",
    },
    "home_welcome": {"en": "Welcome! 👋", "es": "¡Bienvenido! 👋"},
    "home_intro": {
        "en": "Scammers are getting smarter every day.  \n**ShieldFromScam** helps you spot scams before they hurt you.",
        "es": "Los estafadores son cada vez más astutos.  \n**ShieldFromScam** te ayuda a detectar estafas antes de que te hagan daño.",
    },
    "home_features_header": {"en": "🔍 What you can do here:", "es": "🔍 Qué puedes hacer aquí:"},
    "home_table": {
        "en": (
            "| Feature | Description |\n|---|---|\n"
            "| 📩 **Message Analyzer** | Paste a suspicious text, email, or message and get instant feedback |\n"
            "| 🧠 **Scam Quiz** | Test your scam-spotting skills with real-life scenarios |\n"
            "| 📚 **Scam Library** | Learn about the most common scam types |\n"
            "| 📞 **Report a Scam** | Find out where and how to report scams |"
        ),
        "es": (
            "| Función | Descripción |\n|---|---|\n"
            "| 📩 **Analizador de mensajes** | Pega un mensaje sospechoso y obtén análisis instantáneo |\n"
            "| 🧠 **Quiz de estafas** | Pon a prueba tus habilidades para detectar estafas |\n"
            "| 📚 **Biblioteca de estafas** | Aprende sobre los tipos de estafas más comunes |\n"
            "| 📞 **Reportar una estafa** | Descubre dónde y cómo reportar estafas |"
        ),
    },
    "home_howto_header": {"en": "👉 How to get started:", "es": "👉 Cómo empezar:"},
    "home_howto": {
        "en": (
            "1. Click **📩 Message Analyzer** in the sidebar to check a suspicious message.\n"
            "2. Or try the **🧠 Scam Quiz** to see how scam-savvy you are!"
        ),
        "es": (
            "1. Haz clic en **📩 Analizador de mensajes** para revisar un mensaje sospechoso.\n"
            "2. O prueba el **🧠 Quiz de estafas** para ver qué tan bueno eres detectando estafas."
        ),
    },
    "home_tip": {
        "en": "🛡️ Tip: When in doubt — **don't click, don't reply, don't pay.**",
        "es": "🛡️ Consejo: Cuando tengas dudas — **no hagas clic, no respondas, no pagues.**",
    },

    # ── Message Analyzer ───────────────────────────────────────
    "analyzer_title": {"en": "📩 Message Analyzer", "es": "📩 Analizador de Mensajes"},
    "analyzer_intro": {
        "en": (
            "Paste any **suspicious message, email, or text** below and click **Analyze**."
            " Our app will check it for scam warning signs."
        ),
        "es": (
            "Pega cualquier **mensaje, correo o texto sospechoso** abajo y haz clic en **Analizar**."
            " Nuestra app lo revisará en busca de señales de estafa."
        ),
    },
    "analyzer_lang_note": {
        "en": (
            "ℹ️ **Note:** The app translates its own buttons, verdicts, and guidance into Spanish. "
            "Your original message is analyzed as written — the scam score does not change with language."
        ),
        "es": (
            "ℹ️ **Nota:** La app traduce sus propios botones, veredictos y consejos al español. "
            "Tu mensaje original se analiza tal como está escrito — la puntuación no cambia al cambiar el idioma."
        ),
    },
    "example_label": {
        "en": "💡 Need an example? Click here to load one",
        "es": "💡 ¿Necesitas un ejemplo? Haz clic aquí para cargar uno",
    },
    "example_choose": {"en": "Choose an example:", "es": "Elige un ejemplo:"},
    "example_none": {"en": "None", "es": "Ninguno"},
    "example_irs": {"en": "IRS Phone Scam", "es": "Estafa telefónica del IRS"},
    "example_lottery": {"en": "Lottery Winner Scam", "es": "Estafa de lotería"},
    "example_tech": {"en": "Tech Support Scam", "es": "Estafa de soporte técnico"},
    "example_gift": {"en": "Gift Card Scam", "es": "Estafa de tarjetas de regalo"},
    "textarea_label": {
        "en": "✏️ Paste or type the message here:",
        "es": "✏️ Pega o escribe el mensaje aquí:",
    },
    "textarea_placeholder": {
        "en": "Example: 'Congratulations! You have won a $1,000 gift card. Click here to claim your prize now!'",
        "es": "Ejemplo: '¡Felicidades! Has ganado una tarjeta de regalo de $1,000. ¡Haz clic aquí para reclamar tu premio!'",
    },
    "btn_analyze": {"en": "🔍 Analyze", "es": "🔍 Analizar"},
    "btn_clear": {"en": "🗑️ Clear", "es": "🗑️ Limpiar"},
    "warn_empty": {
        "en": "⚠️ Please paste or type a message above before clicking Analyze.",
        "es": "⚠️ Por favor, pega o escribe un mensaje antes de hacer clic en Analizar.",
    },

    # ── Results ────────────────────────────────────────────────
    "results_score_header": {"en": "📊 Risk Score", "es": "📊 Puntuación de Riesgo"},
    "results_score_of": {"en": "Score: {score} / 100", "es": "Puntuación: {score} / 100"},
    "results_verdict_header": {"en": "🏷️ Verdict", "es": "🏷️ Veredicto"},
    "results_warnings_header": {"en": "🚩 Warning Signs Found", "es": "🚩 Señales de Alerta Encontradas"},
    "results_no_warnings": {
        "en": (
            "No known scam phrases were detected. "
            "Always stay cautious — not all scams use obvious keywords!"
        ),
        "es": (
            "No se detectaron frases de estafa conocidas. "
            "¡Mantente siempre alerta — no todas las estafas usan palabras clave obvias!"
        ),
    },
    "results_action_header": {"en": "💡 What should you do?", "es": "💡 ¿Qué debes hacer?"},

    # Verdict strings (must match exactly what analyze_message returns)
    "verdict_safe": {"en": "Looks Safe", "es": "Parece Seguro"},
    "verdict_slightly": {"en": "Slightly Suspicious", "es": "Levemente Sospechoso"},
    "verdict_suspicious": {"en": "Suspicious — Be Careful", "es": "Sospechoso — Ten Cuidado"},
    "verdict_scam": {"en": "Likely a Scam — Do NOT respond", "es": "Probablemente una Estafa — NO respondas"},

    # Advice blocks
    "advice_safe": {
        "en": (
            "- This message appears safe, but always verify unexpected requests.\n"
            "- Never share personal information you weren't expecting to give.\n"
            "- When in doubt, contact the company directly using their **official website**."
        ),
        "es": (
            "- Este mensaje parece seguro, pero siempre verifica solicitudes inesperadas.\n"
            "- Nunca compartas información personal que no esperabas dar.\n"
            "- Ante cualquier duda, contacta a la empresa directamente desde su **sitio web oficial**."
        ),
    },
    "advice_slightly": {
        "en": (
            "- Proceed with caution — a few mild warning signs were found.\n"
            "- Look up the sender's contact info independently — **do NOT use any number or link in the message**.\n"
            "- Ask a trusted friend or family member before responding."
        ),
        "es": (
            "- Procede con precaución — se encontraron algunas señales leves.\n"
            "- Busca la información de contacto del remitente por tu cuenta — **NO uses ningún número o enlace del mensaje**.\n"
            "- Pregunta a un amigo o familiar de confianza antes de responder."
        ),
    },
    "advice_suspicious": {
        "en": (
            "- **Do NOT reply or send any money.**\n"
            "- Look up the company's real contact info independently.\n"
            "- Report to the FTC at [ReportFraud.ftc.gov](https://reportfraud.ftc.gov) (USA).\n"
            "- Ask a trusted adult or call your bank if you're unsure."
        ),
        "es": (
            "- **NO respondas ni envíes dinero.**\n"
            "- Busca la información de contacto real de la empresa por tu cuenta.\n"
            "- Reporta a la FTC en [ReportFraud.ftc.gov](https://reportfraud.ftc.gov) (EE.UU.).\n"
            "- Pregunta a un adulto de confianza o llama a tu banco si tienes dudas."
        ),
    },
    "advice_scam": {
        "en": (
            "- **Do NOT reply, click any links, or call any number in this message.**\n"
            "- Block the sender immediately.\n"
            "- Report the scam at [ReportFraud.ftc.gov](https://reportfraud.ftc.gov) (USA).\n"
            "- If you already responded or sent money, contact your bank right away."
        ),
        "es": (
            "- **NO respondas, no hagas clic en ningún enlace ni llames a ningún número de este mensaje.**\n"
            "- Bloquea al remitente inmediatamente.\n"
            "- Reporta la estafa en [ReportFraud.ftc.gov](https://reportfraud.ftc.gov) (EE.UU.).\n"
            "- Si ya respondiste o enviaste dinero, contacta a tu banco de inmediato."
        ),
    },

    # ── Read Aloud ─────────────────────────────────────────────
    "btn_read_aloud": {"en": "🔊 Read Aloud", "es": "🔊 Leer en Voz Alta"},
    "btn_stop_speaking": {"en": "⏹️ Stop Speaking", "es": "⏹️ Detener Lectura"},
    "read_aloud_unsupported": {
        "en": (
            "⚠️ Your browser does not support text-to-speech. "
            "Try opening this app in Google Chrome or Microsoft Edge."
        ),
        "es": (
            "⚠️ Tu navegador no admite texto a voz. "
            "Intenta abrir esta app en Google Chrome o Microsoft Edge."
        ),
    },

    # ── Analyzer page title (Streamlit page_title) ─────────────
    "analyzer_page_title": {
        "en": "Message Analyzer — ShieldFromScamApp",
        "es": "Analizador de Mensajes — ShieldFromScamApp",
    },
}


def T(lang: str, key: str, **kwargs) -> str:
    """
    Return the translated string for *key* in *lang* ('en' or 'es').
    Falls back to English if the key or language is missing.
    Supports simple format substitutions: T(lang, "key", score=42)
    """
    entry = _STRINGS.get(key, {})
    text = entry.get(lang) or entry.get("en") or f"[{key}]"
    if kwargs:
        text = text.format(**kwargs)
    return text
