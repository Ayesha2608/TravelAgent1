import os
import streamlit as st
from chatbot import get_reply
from services.weather import get_weather

st.set_page_config(
    page_title="PlanGuard | Your Travel Companion",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
:root {
  --ink: #30294f; --muted: #817895; --pink: #e98eaf; --pink-dark: #c85e91;
  --lilac: #eee7fa; --cream: #fffaf8; --line: #f0dce9;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
/* Explicitly override Streamlit's active theme so text stays readable in light mode. */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
  background: linear-gradient(135deg, #fffaf8 0%, #fff7fb 48%, #f6f0ff 100%) !important;
  color: #30294f !important;
}
.stApp p, .stApp span, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stApp h5, .stApp h6, .stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stCaptionContainer"] { color: #30294f; }
.stApp [data-testid="stCaptionContainer"] { color: #756b89 !important; }
header[data-testid="stHeader"] { background: rgba(255,250,248,.96) !important; }
[data-testid="stToolbar"] { background: transparent !important; }
.block-container { max-width: 1450px; padding-top: 1.5rem; padding-bottom: 7rem; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#fff5f8 0%,#f7f1ff 100%) !important; border-right: 1px solid var(--line); }
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; background: transparent !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: var(--ink) !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: #514665 !important; }
.plan-logo { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #30294f; letter-spacing: -.5px; margin-bottom: -.2rem; }
.plan-subtitle { color: var(--muted); font-size: .95rem; margin-bottom: 1.2rem; }
.hero { text-align: center; padding: 1.7rem 1rem 1.2rem; border: 1px solid rgba(240,220,233,.8); border-radius: 28px; background: linear-gradient(135deg,rgba(255,255,255,.9),rgba(255,245,251,.82)); box-shadow: 0 12px 40px rgba(105,76,125,.06); margin-bottom: 1.3rem; }
.hero-kicker { display: inline-block; border-radius: 999px; background: #f3eafa; color: #8a65a9; padding: .38rem .8rem; font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.hero h1 { font-family: 'Playfair Display',serif; color: var(--ink); font-size: clamp(2.2rem,4vw,3.2rem); margin: .65rem 0 .2rem; }
.hero p { color: var(--muted); font-size: 1.02rem; margin-bottom: .8rem; }
.pill-row { display:flex; flex-wrap:wrap; gap:.55rem; justify-content:center; margin-top:.8rem; }
.pill { background:#fff; border:1px solid #f0dce9; color:#75658f; padding:.45rem .75rem; border-radius:999px; font-size:.82rem; }
.feature-card { background: rgba(255,255,255,.82); border: 1px solid var(--line); border-radius: 18px; padding: 1rem 1.05rem; min-height: 100px; box-shadow: 0 7px 22px rgba(105,76,125,.045); }
.feature-icon { font-size:1.35rem; }
.feature-title { color:var(--ink); font-weight:700; margin:.25rem 0 .15rem; }
.feature-copy { color:var(--muted); font-size:.84rem; line-height:1.45; }
.stButton > button, .stDownloadButton > button { border-radius: 13px; border: 1px solid #ebcddd; background: linear-gradient(135deg,#f5b7ce,#e8c8ef); color:#493354; font-weight:700; transition: all .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#d990b3; color:#30294f; transform:translateY(-1px); }
.stButton > button p, .stDownloadButton > button p { color:#493354 !important; }
[data-testid="stMetric"] { color:#30294f !important; }
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] { color:#30294f !important; }
[data-testid="stDataFrame"] { background:#ffffff !important; }
[data-testid="stExpander"] { background:rgba(255,255,255,.7) !important; border-color:#f0dce9 !important; }
.stTextInput input, .stTextArea textarea {
  border-radius: 13px !important; border:1px solid #ead8e7 !important;
  background:#ffffff !important; color:#30294f !important; -webkit-text-fill-color:#30294f !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder { color:#817895 !important; opacity:1 !important; -webkit-text-fill-color:#817895 !important; }
[data-testid="stChatMessage"] { border:1px solid #f0dfeb; border-radius:20px; padding:.9rem 1rem; box-shadow:0 6px 20px rgba(105,76,125,.035); margin-bottom:.8rem; color:#30294f !important; }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color:#30294f !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background:linear-gradient(135deg,#fff,#f5eafa) !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { background:rgba(255,255,255,.96) !important; }
/* Keep the fixed composer area pastel instead of inheriting Streamlit's dark footer. */
[data-testid="stBottom"], [data-testid="stBottom"] > div,
[data-testid="stChatInput"] > div, [data-testid="stChatInput"] form {
  background:rgba(255,250,248,.97) !important;
  background-color:rgba(255,250,248,.97) !important;
}
[data-testid="stChatInput"] {
  border:1px solid #ebd5e7 !important; border-radius:22px !important;
  background:#ffffff !important; background-color:#ffffff !important;
  box-shadow:0 8px 28px rgba(105,76,125,.08);
}
[data-testid="stChatInput"] textarea {
  background:#ffffff !important; background-color:#ffffff !important;
  color:#30294f !important; -webkit-text-fill-color:#30294f !important;
}
[data-testid="stChatInput"] button { background:#f1c1d7 !important; color:#493354 !important; }
hr { border-color:#f0dce9; }
.stMetric { background:rgba(255,255,255,.72); border:1px solid var(--line); padding:.7rem; border-radius:15px; }
div[data-testid="stAlert"] { border-radius:14px; }
footer { visibility:hidden; }
@media (max-width: 800px) { .hero { padding:1.2rem .7rem; } .block-container { padding-top:1rem; } }
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "weather" not in st.session_state:
    st.session_state.weather = None
if "weather_place" not in st.session_state:
    st.session_state.weather_place = None
if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = ""

# In local development use .streamlit/secrets.toml; on Cloud use app Secrets.
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="plan-logo">✈ PlanGuard</div><div class="plan-subtitle">Your AI travel companion ✨</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📝 Your trip notes")
    st.caption("Add details once and PlanGuard can use them throughout this session.")
    trip_notes = st.text_area(
        "Trip requirements",
        placeholder="Origin: Karachi\nDestination: Hunza\nTravellers: 4\nBudget: PKR 250,000\nDates: flexible",
        height=155,
        key="trip_notes",
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 🌦️ Live weather")
    st.caption("Check current conditions and the short-term forecast.")
    place = st.text_input("Destination", placeholder="e.g. Gilgit", label_visibility="collapsed", key="weather_destination")
    if st.button("☁️  Check weather", use_container_width=True):
        if not place.strip():
            st.warning("Enter a city or destination first.")
        else:
            try:
                with st.spinner("Checking the skies…"):
                    st.session_state.weather = get_weather(place.strip())
                    st.session_state.weather_place = place.strip()
            except Exception as exc:
                st.session_state.weather = None
                st.error(f"Weather lookup failed: {exc}")
    if st.session_state.weather:
        weather = st.session_state.weather
        st.success(f"Weather for {weather['place']}")
        st.metric("Temperature now", f"{weather['current']['temperature_2m']} °C")
        st.caption("Forecast covers the next five days. Source: Open-Meteo.")
        with st.expander("View forecast details"):
            st.dataframe(weather["daily"], hide_index=True, use_container_width=True)
        if st.button("Clear weather", use_container_width=True):
            st.session_state.weather = None
            st.session_state.weather_place = None
            st.rerun()
    st.markdown("---")
    st.markdown("### 💌 Your conversation")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.session_state.messages:
        chat_text = "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages)
        st.download_button("↓  Download chat (.txt)", chat_text, "planguard_chat.txt", "text/plain", use_container_width=True)
    st.markdown("<div style='color:#9b8da9;font-size:.75rem;padding-top:1rem'>Made for curious minds and faraway places ♡</div>", unsafe_allow_html=True)

# ---------- Main content ----------
st.markdown('''<div class="hero">
  <span class="hero-kicker">✦ Your next chapter starts here</span>
  <h1>Let's plan somewhere beautiful.</h1>
  <p>Thoughtful itineraries, practical travel advice, and a little more confidence before you go.</p>
  <div class="pill-row"><span class="pill">✧ Personalised itineraries</span><span class="pill">☼ Live weather</span><span class="pill">⌁ Budget-aware ideas</span><span class="pill">♡ Flexible plans</span></div>
</div>''', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("#### A little inspiration for your next trip")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><div class="feature-icon">🏔️</div><div class="feature-title">Find your destination</div><div class="feature-copy">Compare places based on your vibe, budget, and travel dates.</div></div>', unsafe_allow_html=True)
        if st.button("Help me choose a destination", key="choose_destination", use_container_width=True):
            st.session_state.suggested_prompt = "Help me choose a destination based on my interests, budget, travel dates, and starting city. Ask me what you need to know."
            st.rerun()
    with c2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🗺️</div><div class="feature-title">Build an itinerary</div><div class="feature-copy">Create a realistic day-by-day plan with transport and stays.</div></div>', unsafe_allow_html=True)
        if st.button("Plan a full trip", key="plan_trip", use_container_width=True):
            st.session_state.suggested_prompt = "Help me build a complete trip plan including itinerary, transport, accommodation, estimated costs, and backup options. Ask me for missing details."
            st.rerun()
    with c3:
        st.markdown('<div class="feature-card"><div class="feature-icon">🌦️</div><div class="feature-title">Check before you go</div><div class="feature-copy">Consider weather, timing, and practical alternatives before travelling.</div></div>', unsafe_allow_html=True)
        if st.button("Prepare for my trip", key="prepare_trip", use_container_width=True):
            st.session_state.suggested_prompt = "Help me prepare for my trip. Review weather considerations, transport, packing, safety, budget risks, and backup plans. Ask me for my destination and dates."
            st.rerun()
    st.markdown("\n")

if not api_key:
    st.error("Missing GROQ_API_KEY. Add it to `.streamlit/secrets.toml` locally or to your Streamlit app Secrets.")
    st.stop()

# Render conversation history.
for message in st.session_state.messages:
    avatar = "🧭" if message["role"] == "assistant" else "🌸"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# A feature-card click can seed the next chat turn.
prompt = st.session_state.suggested_prompt
user_text = st.chat_input("Tell me where you're dreaming of going…")
if not user_text and prompt:
    user_text = prompt
    st.session_state.suggested_prompt = ""

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="🌸"):
        st.markdown(user_text)
    with st.chat_message("assistant", avatar="🧭"):
        with st.spinner("Putting your plan together…"):
            try:
                reply = get_reply(
                    api_key,
                    st.session_state.messages,
                    trip_notes=trip_notes,
                    weather=st.session_state.weather,
                )
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as exc:
                st.error("Could not get a response. Check your API key, model access, usage limits, and connection.")
                with st.expander("Technical details"):
                    st.code(str(exc))
