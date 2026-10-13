# ==============================================================
# pages/5_About.py
# Page 5 — About ShieldFromScamApp
# v6: Defensive rewrite — no attribute errors can reach the user.
#     All key lookups guarded. Fallback content shown on any error.
#     Language selector preserved.
# ==============================================================

import streamlit as st
import sys
import os

# ── Safe import of translations ───────────────────────────────────────────────
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.translations import T
    _translations_ok = True
except Exception:
    _translations_ok = False
    def T(lang, key, **kw):  # fallback no-op
        return key

st.set_page_config(
    page_title="About — ShieldFromScamApp",
    page_icon="ℹ️",
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
try:
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    st.sidebar.title("🛡️ ShieldFromScamApp")
    st.sidebar.markdown("---")
    lang_choice = st.sidebar.radio(
        "🌐 Language / Idioma",
        options=["English", "Español"],
        index=0 if st.session_state.get("lang", "en") == "en" else 1,
        key="lang_radio_about",
    )
    st.session_state["lang"] = "en" if lang_choice == "English" else "es"
    lang = st.session_state["lang"]
except Exception:
    lang = "en"

# ── UI string table (self-contained — does NOT rely on translations.py) ───────
_UI = {
    "en": {
        "title": "About ShieldFromScamApp",
        "tip": "Stay safe out there. When in doubt — slow down, verify, and ask for help.",
        "body": """
### What is ShieldFromScamApp?

**ShieldFromScamApp** is a free, beginner-friendly web app that helps everyday people —
especially seniors and those less familiar with technology — identify potential scams in
text messages, emails, and other written communications.

---

### How It Works

Paste any suspicious message into the **Message Analyzer**. The app will return:

- **A risk score** from 0 to 100
- **A verdict** (Looks Safe / Slightly Suspicious / Suspicious / Likely a Scam)
- **A risk level** shown with a color-coded bar
- **An explanation** of each warning sign detected and why it matters
- **Safety recommendations** for what to do next

The app uses a **3-layer context-aware detection engine** — no internet connection or
paid API is required. Your message stays on your own device.

---

### Safety Tips

- Always verify suspicious messages independently — call the company or agency directly
  using a phone number you look up yourself, not one from the message.
- Never click links or call numbers from unexpected messages before checking.
- Never share passwords, verification codes, or Social Security numbers with anyone
  who contacted you first.
- When in doubt, ask a trusted friend, family member, or your bank before responding.

---

### Limitations

- **Detection is not perfect.** The app uses pattern matching, not human judgment.
  A low score does not guarantee a message is safe, and some scams may not trigger
  any known patterns.
- **Results are not legal or financial advice.** Always use your own judgment and
  verify independently.
- The app works best with English-language messages. Spanish interface is available
  but the detection engine analyzes the original message text.

---

### Features

| Feature | Description |
|---|---|
| 📩 Message Analyzer | Paste any suspicious text, email, or call script for instant analysis |
| 🔊 Read Aloud | Hear the risk score, warning signs, and safety advice read aloud |
| 🌐 English / Spanish | Switch the app interface between English and Español |
| 🧠 Scam Quiz | 8-question interactive quiz to sharpen your scam awareness |
| 📚 Scam Library | Plain-language guides to 8 major scam types |
| 📞 Report a Scam | Direct links to all major US fraud reporting agencies |

---

### Congressional App Challenge — District 6

This app was created for the **2026 Congressional App Challenge**, representing
**Congressional District 6**.

The challenge encourages students to build apps that solve real problems in their
communities. ShieldFromScamApp addresses the growing epidemic of financial fraud
targeting American families.

---

### Built With

- **Python** — programming language
- **Streamlit** — web app framework
- **Browser Web Speech API** — powers the free Read Aloud feature (no paid API needed)
- **No paid APIs or external services** — runs entirely on your device

---
""",
    },
    "es": {
        "title": "Acerca de ShieldFromScamApp",
        "tip": "Cuídate. Cuando tengas dudas — tómate tu tiempo, verifica y pide ayuda.",
        "body": """
### ¿Qué es ShieldFromScamApp?

**ShieldFromScamApp** es una aplicación web gratuita y fácil de usar que ayuda a las
personas comunes — especialmente a adultos mayores y a quienes tienen menos experiencia
con la tecnología — a identificar posibles estafas en mensajes de texto, correos
electrónicos y otras comunicaciones escritas.

---

### Cómo Funciona

Pega cualquier mensaje sospechoso en el **Analizador de Mensajes**. La app te dará:

- **Una puntuación de riesgo** de 0 a 100
- **Un veredicto** (Parece Seguro / Levemente Sospechoso / Sospechoso / Probablemente una Estafa)
- **Un nivel de riesgo** mostrado con una barra de colores
- **Una explicación** de cada señal de alerta detectada y por qué importa
- **Recomendaciones de seguridad** sobre qué hacer a continuación

La app usa un **motor de detección contextual de 3 capas** — no necesita conexión a
internet ni API de pago. Tu mensaje permanece en tu propio dispositivo.

---

### Consejos de Seguridad

- Siempre verifica los mensajes sospechosos de forma independiente — llama a la empresa
  o agencia directamente usando un número que busques tú mismo, no el del mensaje.
- Nunca hagas clic en enlaces ni llames a números de mensajes inesperados sin verificar primero.
- Nunca compartas contraseñas, códigos de verificación ni números de Seguro Social con
  alguien que te contactó primero.
- Cuando tengas dudas, consulta a un amigo de confianza, familiar o tu banco antes de responder.

---

### Limitaciones

- **La detección no es perfecta.** La app usa reconocimiento de patrones, no juicio humano.
  Una puntuación baja no garantiza que un mensaje sea seguro, y algunas estafas pueden
  no activar ningún patrón conocido.
- **Los resultados no son asesoramiento legal ni financiero.** Siempre usa tu propio
  juicio y verifica de forma independiente.
- La app funciona mejor con mensajes en inglés. La interfaz en español está disponible,
  pero el motor de detección analiza el texto del mensaje original.

---

### Funciones

| Función | Descripción |
|---|---|
| 📩 Analizador de Mensajes | Pega cualquier texto, correo o mensaje sospechoso para análisis instantáneo |
| 🔊 Leer en Voz Alta | Escucha la puntuación, señales de alerta y consejos leídos en voz alta |
| 🌐 Inglés / Español | Cambia la interfaz entre English y Español |
| 🧠 Quiz de Estafas | Quiz interactivo de 8 preguntas para mejorar tu conciencia |
| 📚 Biblioteca de Estafas | Guías en lenguaje sencillo sobre 8 tipos principales de estafas |
| 📞 Reportar una Estafa | Enlaces directos a las principales agencias de denuncia de fraudes en EE.UU. |

---

### Desafío de Apps del Congreso — Distrito 6

Esta aplicación fue creada para el **Desafío de Apps del Congreso 2026**, representando
el **Distrito Congresional 6**.

---

### Construida con

- **Python** — lenguaje de programación
- **Streamlit** — framework de aplicaciones web
- **API de Voz del Navegador** — función gratuita de Leer en Voz Alta (sin API de pago)
- **Sin APIs de pago ni servicios externos** — funciona completamente en tu dispositivo

---
""",
    },
}


def _get(key: str) -> str:
    """Safely retrieve a UI string; fall back to English, then to the key name."""
    try:
        return _UI.get(lang, _UI["en"]).get(key) or _UI["en"].get(key) or key
    except Exception:
        return key


# ── Page content ──────────────────────────────────────────────────────────────
try:
    st.title(_get("title"))
    st.markdown("---")
    st.markdown(_get("body"))
    st.info(_get("tip"))
except Exception as e:
    # Last-resort fallback: show friendly message, never a raw traceback
    st.title("About ShieldFromScamApp")
    st.markdown("---")
    st.markdown("""
**ShieldFromScamApp** is a free app that helps you identify potential scams in
text messages and emails.

Paste any suspicious message into the **Message Analyzer** to get a risk score,
verdict, and safety advice.

**Important:** A low score does not guarantee a message is safe. Always verify
suspicious messages independently.
""")
    st.info("Stay safe. When in doubt — slow down, verify, and ask for help.")
