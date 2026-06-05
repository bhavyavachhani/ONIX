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

# 2. Tracking First-Time Page Load Animation State
if "animated" not in st.session_state:
    st.session_state.animated = False

# 3. Clean Site Loading Animation Sequence
title_placeholder = st.empty()

if not st.session_state.animated:
    # Simulates a clean terminal typing effect for the name
    name_string = "ONIX"
    typed_name = ""
    for letter in name_string:
        typed_name += letter
        title_placeholder.markdown(f"## {typed_name}")
        time.sleep(0.15)  # Controls typing speed
    time.sleep(0.2)
    st.session_state.animated = True
else:
    # Immediately displays the clean header text on subsequent script reruns
    title_placeholder.markdown("## ONIX")

# 4. Secure API Key Retrieval
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Authentication Missing. System offline.")
    st.stop()

client = Groq(api_key=api_key)

# 5. Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Render Chat Logs Instantly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Prompt Box Input & Pipeline
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