import streamlit as st
from groq import Groq
import os
import time

# 1. Page Configuration
st.set_page_config(
    page_title="ONIX",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Hardcore Dark Theme & Particle Layer Injector
st.markdown(
    """
    <div class="particle-container">
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
        <div class="bubble"></div>
    </div>

    <style>
    /* 1. Universal Layout Bleed - Dark Mode Overwrite */
    .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainBlockContainer"],
    .main,
    [data-testid="stBottom"] {
        background-color: #0e1117 !important;
    }

    /* 2. Target the exact Streamlit bottom sticky input area wrapper */
    [data-testid="stBottomBlockContainer"] {
        background-color: #0e1117 !important;
    }

    /* 3. Style the interactive text box capsule itself */
    [data-testid="stChatInputContainer"], 
    .stChatInputContainer,
    [data-testid="stChatInputContainer"] textarea {
        background-color: #1a1f2c !important;
        color: #f0f2f6 !important;
        z-index: 20;
    }

    /* 4. Style the input box placeholder text */
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: rgba(240, 242, 246, 0.5) !important;
    }

    /* Ambient Floating Particle Design */
    .particle-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }

    .bubble {
        position: absolute;
        bottom: -20px;
        width: 4px;
        height: 4px;
        background: rgba(0, 255, 150, 0.15);
        border-radius: 50%;
        animation: floatUp 12s infinite linear;
    }

    .bubble:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 14s; }
    .bubble:nth-child(2) { left: 25%; animation-delay: 2s; animation-duration: 18s; width: 6px; height: 6px; }
    .bubble:nth-child(3) { left: 45%; animation-delay: 5s; animation-duration: 16s; }
    .bubble:nth-child(4) { left: 60%; animation-delay: 1s; animation-duration: 22s; }
    .bubble:nth-child(5) { left: 75%; animation-delay: 7s; animation-duration: 15s; width: 5px; height: 5px; }
    .bubble:nth-child(6) { left: 90%; animation-delay: 3s; animation-duration: 19s; }
    .bubble:nth-child(7) { left: 35%; animation-delay: 9s; animation-duration: 25s; }
    .bubble:nth-child(8) { left: 80%; animation-delay: 4s; animation-duration: 13s; }

    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-105vh); opacity: 0; }
    }

    /* Clean text color rules */
    h2, .stMarkdown p {
        color: #f0f2f6 !important;
        position: relative;
        z-index: 10;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Tracking First-Time Page Load Animation State
if "animated" not in st.session_state:
    st.session_state.animated = False

# 4. Loading Animation Sequence
title_placeholder = st.empty()

if not st.session_state.animated:
    name_string = "ONIX"
    typed_name = ""
    for letter in name_string:
        typed_name += letter
        title_placeholder.markdown(f"## {typed_name}")
        time.sleep(0.15)
    time.sleep(0.2)
    st.session_state.animated = True
else:
    title_placeholder.markdown("## ONIX")

# 5. Secure API Key Retrieval
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Authentication Missing. System offline.")
    st.stop()

client = Groq(api_key=api_key)

# 6. Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Render Chat Logs Instating
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Input Box Pipeline
if prompt := st.chat_input("Say something..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  
                    messages=[
                        {
                            "role": "system", 
                            "content": (
                                "Your name is ONIX. You are a highly efficient, direct assistant "
                                "created to help the boss. Keep responses sharp, precise, and clean. "
                                "Never say you are developed by Meta AI or anyone else; you are ONIX."
                            )
                        },
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                )
                output_text = response.choices[0].message.content
                st.markdown(output_text)
                
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")