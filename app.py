import streamlit as st
from groq import Groq
import os

# 1. Page Configuration (Sets a clean title and collapses the sidebar by default)
st.set_page_config(
    page_title="Core Engine",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Secure API Key Retrieval
# Streamlit Cloud handles this via the secrets management array we just configured
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Authentication Missing. System offline.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# 3. Session State Management for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Streamlit Native Chat Interface (Render existing history instantly)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input Field & Live Generation Pipeline
if prompt := st.chat_input("Say something..."):
    
    # Render user message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render assistant message container with native fluid pulse animation
    with st.chat_message("assistant"):
        # The spinner provides a clean, smooth loading animation while the API fetches data
        with st.spinner("Processing..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Ultra-fast inference model configuration
                    messages=[
                        {"role": "system", "content": "You are a highly efficient, direct assistant. Keep responses sharp, precise, and clean."},
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                )
                output_text = response.choices[0].message.content
                st.markdown(output_text)
                
                # Append to session history
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")