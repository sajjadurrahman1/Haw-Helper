# haw_helper_ui.py
import streamlit as st
import datetime
import json
import numpy as np
import faiss
import langid
from openai import OpenAI

# --- CONFIG ---
LOGO_PATH = "haw-logo.png"
HAW_BLUE = "#004B87"
HAW_LIGHT = "#E6F0FA"
HAW_GRAY = "#F7F7F7"

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# --- OPENAI CLIENT ---
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", None))

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="HAW-Helper", page_icon=LOGO_PATH, layout="wide")

# --- LOAD INDEXES ---
@st.cache_resource
def load_indexes():
    def load_one(lang):
        index = faiss.read_index(f"haw_kb_{lang}.index")
        with open(f"haw_kb_meta_{lang}.json", "r", encoding="utf-8") as f:
            meta = json.load(f)
        return index, meta

    en_index, en_meta = load_one("en")
    de_index, de_meta = load_one("de")
    return {"en": (en_index, en_meta), "de": (de_index, de_meta)}

indexes = load_indexes()

# --- CUSTOM CSS ---
st.markdown(
    f"""
    <style>
    body {{ background-color: {HAW_GRAY}; }}
    .main-title {{ font-size: 2rem; font-weight: 600; color: {HAW_BLUE}; }}
    .subtitle {{ font-size: 1rem; color: #444; margin-bottom: 1rem; }}
    .chat-bubble-user {{
        background-color: {HAW_BLUE}; color: white;
        padding: 10px 15px; border-radius: 18px 18px 0 18px;
        margin: 5px 0; max-width: 70%; float: right; clear: both;
    }}
    .chat-bubble-assistant {{
        background-color: {HAW_LIGHT}; color: black;
        padding: 10px 15px; border-radius: 18px 18px 18px 0;
        margin: 5px 0; max-width: 70%; float: left; clear: both;
    }}
    .footer {{ text-align: center; font-size: 0.85rem; color: #666; margin-top: 2rem; }}
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
st.sidebar.info("💡 Ask about courses, exams, deadlines, or admissions.")

# --- CHAT STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("### 💬 Chat with HAW-Helper")

# --- DISPLAY CHAT ---
chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        bubble_class = "chat-bubble-user" if role == "user" else "chat-bubble-assistant"
        prefix = f"<b>HAW-Helper ({personality}):</b><br>" if role == "assistant" else ""
        st.markdown(f'<div class="{bubble_class}">{prefix}{message}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
user_input = st.text_area("✏️ Type your question here:", key="chat_input", height=80)
colA, colB = st.columns([1, 5])
send_btn = colA.button("Send", type="primary")
clear_btn = colB.button("Clear Chat")

# --- FUNCTION: SEARCH KB ---
def search_kb(query, lang):
    index, meta = indexes[lang]
    q_embed = client.embeddings.create(model=EMBED_MODEL, input=query).data[0].embedding
    q_vec = np.array(q_embed, dtype="float32").reshape(1, -1)
    D, I = index.search(q_vec, k=4)
    matches = [meta["texts"][i] for i in I[0] if i < len(meta["texts"])]
    return matches, D[0][0]

# --- FUNCTION: AI RESPONSE ---
def generate_answer(query, lang):
    matches, score = search_kb(query, lang)
    if not matches or score > 2.0:
        return "Sorry, I couldn’t find that information in my knowledge base."

    context = "\n\n".join(matches)
    prompt = f"""
    You are HAW-Helper, an assistant for Hamburg University of Applied Sciences.
    Answer the following question using ONLY the provided context.
    If the answer is not clearly in the context, say: 
    "Sorry, I couldn’t find that information in my knowledge base."

    Context:
    {context}

    Question: {query}
    """
    completion = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "system", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()

# --- HANDLE INPUT ---
if send_btn and user_input.strip():
    user_message = user_input.strip()
    st.session_state.chat_history.append(("user", user_message))

    # detect language of question
    lang, _ = langid.classify(user_message)
    lang = "de" if lang == "de" else "en"

    response = generate_answer(user_message, lang)
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()

if clear_btn:
    st.session_state.chat_history = []
    st.rerun()

# --- FOOTER ---
st.markdown(
    f'<div class="footer">© {datetime.date.today().year} HAW Hamburg • HAW-Helper Prototype</div>',
    unsafe_allow_html=True
)