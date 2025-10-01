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