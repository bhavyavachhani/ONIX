import streamlit as st
from groq import Groq
import os

# 1. Page Configuration (Sets a clean browser title and collapses the sidebar)
st.set_page_config(
    page_title="Core Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Secure API Key Retrieval from Streamlit Cloud Secrets Management
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Authentication Missing. System offline.")
    st.stop()

# Initialize Groq client with the verified key string
client = Groq(api_key=api_key)

# 3. Session State Management for Tracking Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Streamlit Native Chat Interface (Renders previous message blocks instantly)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input Field Matrix & Live Generation Pipeline
if prompt := st.chat_input("Say something..."):
    
    # Render user prompt message instantly onto the screen
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render assistant container with native processing spinner animation
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                # Execution call targeting Groq's active production fast inference model
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",  
                    messages=[
                        {"role": "system", "content": "You are a highly efficient, direct assistant. Keep responses sharp, precise, and clean."},
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                )
                output_text = response.choices[0].message.content
                st.markdown(output_text)
                
                # Append response block into session logs
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")