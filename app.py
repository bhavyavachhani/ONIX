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

# 2. Inject Custom Gemini-Inspired Shifting Gradient Background CSS
st.markdown(
    """
    <style>
    /* Gradient keyframe animation for the background canvas */
    @keyframes geminiFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #131314, #18122B, #0F172A, #131314) !important;
        background-size: 400% 400% !important;
        animation: geminiFlow 15s ease infinite !important;
    }
    
    /* Clean text styling to contrast beautifully against the deep tones */
    h2 {
        color: #e3e3e3 !important;
        font-family: "Google Sans", Arial, sans-serif;
        font-weight: 500 !important;
        letter-spacing: -0.5px;
    }
    
    .stMarkdown p {
        color: #e3e3e3 !important;
    }

    /* Make the default input field frame blend cleanly into the canvas background */
    .stChatInputContainer {
        background-color: rgba(30, 30, 32, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Tracking First-Time Page Load Animation State
if "animated" not in st.session_state:
    st.session_state.animated = False

# 4. Clean Site Loading Animation Sequence
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

# 7. Render Chat Logs Instantly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Prompt Box Input & Pipeline
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