# haw_helper_ui.py
import streamlit as st
import datetime

LOGO_PATH = "haw-logo.png"

# HAW Hamburg Colors
HAW_BLUE = "#004B87"
HAW_LIGHT = "#E6F0FA"
HAW_GRAY = "#F7F7F7"

st.set_page_config(
    page_title="HAW-Helper",
    page_icon=LOGO_PATH,
    layout="wide"
)
# --- CUSTOM CSS ---
st.markdown(
    f"""
    <style>
    body {{
        background-color: {HAW_GRAY};
    }}
    .main-title {{
        font-size: 2rem;
        font-weight: 600;
        color: {HAW_BLUE};
    }}
    .subtitle {{
        font-size: 1rem;
        color: #444;
        margin-bottom: 1rem;
    }}
    .chat-bubble-user {{
        background-color: {HAW_BLUE};
        color: white;
        padding: 10px 15px;
        border-radius: 18px 18px 0 18px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }}
    .chat-bubble-assistant {{
        background-color: {HAW_LIGHT};
        color: black;
        padding: 10px 15px;
        border-radius: 18px 18px 18px 0;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }}
    .footer {{
        text-align: center;
        font-size: 0.85rem;
        color: #666;
        margin-top: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- HEADER ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image(LOGO_PATH, width=120)
with col2:
    st.markdown('<div class="main-title">HAW-Helper</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your friendly assistant for curricula, exams, registration deadlines, and international enrollment support.</div>', unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Settings")
personality = st.sidebar.selectbox(
    "Chatbot Personality",
    ["Friendly & Conversational", "Professional but Warm", "Short & Direct", "Enthusiastic"]
)

st.sidebar.info("💡 Try asking about curriculum, exam registration, or international admission process.")

# --- CHAT INTERFACE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("### 💬 Chat with HAW-Helper")

chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f'<div class="chat-bubble-user">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-assistant"><b>HAW-Helper ({personality}):</b><br>{message}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

user_input = st.text_area("✏️ Type your question here:", key="chat_input", height=80)

colA, colB = st.columns([1, 5])
with colA:
    send_btn = st.button("Send", type="primary")
with colB:
    clear_btn = st.button("Clear Chat")

if send_btn and user_input.strip():
    st.session_state.chat_history.append(("user", user_input.strip()))
    # dummy assistant response (placeholder)
    response = f"I understand your question about **{user_input.strip()}**. Let me fetch the relevant information for you."
    st.session_state.chat_history.append(("assistant", response))
    st.experimental_rerun()

if clear_btn:
    st.session_state.chat_history = []
    st.experimental_rerun()

# --- FOOTER ---
st.markdown(
    f'<div class="footer">© {datetime.date.today().year} HAW Hamburg • HAW-Helper Prototype</div>',
    unsafe_allow_html=True
)
