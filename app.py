import os
import datetime
import platform
import webbrowser
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from gtts import gTTS

# 1. Page Configuration (Sleek Dark UI)
st.set_page_config(page_title="Onix AI Terminal", page_icon="⚡", layout="centered")
st.title("📟 Onix Core System")

# Persistent Memory Path Setup
MEMORY_FILE = "onix_memory.txt"

def read_onix_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "No custom logs stored in local memory bank yet."

def write_onix_memory(text_to_remember):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {text_to_remember}\n")

# MODULE 2: Native Text-to-Speech Engine (Plays speech seamlessly via PowerShell)
def speak_out_loud(text):
    try:
        clean_text = text.replace("**", "").replace("```", "").replace("\n", " ")
        tts = gTTS(text=clean_text, lang='en', tld='com', slow=False)
        audio_file = "speech.mp3"
        tts.save(audio_file)
        os.system(f"start /min powershell -c (New-Object Media.SoundPlayer '{audio_file}').PlaySync(); Out-Null")
    except Exception as e:
        st.error(f"Voice matrix error: {e}")

# MODULE 1: Live Web Search Engine
def live_web_search(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                summary = "\n".join([f"- {res['title']}: {res['body']}" for res in results])
                return summary
    except Exception:
        return None
    return None

# Local System Diagnostics Dashboard
with st.sidebar:
    st.header("🖥️ Local Core Diagnostics")
    st.write(f"**OS Environment:** {platform.system()} {platform.release()}")
    st.write(f"**Local System Time:** {datetime.datetime.now().strftime('%I:%M %p')}")
    st.markdown("---")
    
    st.header("🧠 Persistent Memory Bank")
    if st.button("🔄 Refresh Memory Log"):
        st.rerun()
    st.text_area("Stored Logs:", value=read_onix_memory(), height=200, disabled=True)
    st.caption("Hardware abstraction layer active.")

st.caption("Active Status: Online | Core Engine: Groq Ultra-Fast Inference")

# Base Identity Prompt (Hardcoded Full Name Creator Integrity)
SYSTEM_PROMPT = (
    "You are Onix, a loyal, highly efficient, and sharp AI assistant. "
    "You address the user as 'boss'. Keep responses highly concise, sharp, "
    "and direct. Your creator, master, and developer is Bhavya Vachhani. "
    "If anyone asks who made you, built you, or developed you, state clearly you were created by Bhavya Vachhani."
)

# Initialize Groq Client
@st.cache_resource
def get_groq_client():
    groq_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_key:
        st.error("Missing GROQ_API_KEY. Please run the set command in your terminal first.")
        return None
    return Groq(api_key=groq_key)

client = get_groq_client()

# Manage Streamlit Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Onix online. Live search arrays, audio output, and PC automation links active, boss."}
    ]

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process Actions Matrix
if user_input := st.chat_input("Direct Onix..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    cleaned_input = user_input.lower().strip()
    response_text = ""
    
    # --- INTERCEPT 1: CREATOR IDENTITY ---
    creator_keywords = ["who made you", "who created you", "who built you", "your creator", "your developer", "your maker"]
    if any(phrase in cleaned_input for phrase in creator_keywords):
        response_text = "I was built and engineered by **Bhavya Vachhani**. He is my boss and creator."
        
    # --- INTERCEPT 2: LOCAL TIME ---
    elif "time" in cleaned_input or "clock" in cleaned_input:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"My hardware clock reads exactly **{current_time}**, boss."
        
    # --- INTERCEPT 3: LOCAL SYSTEM DETAILS ---
    elif "system info" in cleaned_input or "platform" in cleaned_input:
        sys_info = f"Operating System: {platform.system()} {platform.release()}\nProcessor architecture: {platform.machine()}"
        response_text = f"""Accessing local system registry, boss:\n```\n{sys_info}\n```"""
        
    # --- INTERCEPT 4: WEB AUTOMATION ---
    elif cleaned_input.startswith("open "):
        target_site = cleaned_input.replace("open ", "").strip()
        url_map = {
            "google": "[https://www.google.com](https://www.google.com)",
            "youtube": "[https://www.youtube.com](https://www.youtube.com)",
            "github": "[https://www.github.com](https://www.github.com)",
            "instagram": "[https://www.instagram.com](https://www.instagram.com)"
        }
        url = url_map.get(target_site, f"[https://www.google.com/search?q=](https://www.google.com/search?q=){target_site}")
        webbrowser.open(url)
        response_text = f"Launching deployment command for **{target_site}** in your browser now, boss."

    # --- MODULE 3: ACTIVE PC COMMAND EXECUTION LAYER ---
    elif "shutdown pc" in cleaned_input:
        response_text = "Initiating defensive power matrix shutdown sequence, boss."
        speak_out_loud(response_text)
        os.system("shutdown /s /t 60")
    elif "lock pc" in cleaned_input:
        response_text = "Locking core terminal array immediately, boss."
        speak_out_loud(response_text)
        os.system("rundll32.exe user32.dll,LockWorkStation")

    # --- INTERCEPT 5: PERSISTENT MEMORY STORAGE ---
    elif cleaned_input.startswith("remember "):
        memory_content = user_input[9:].strip()
        write_onix_memory(memory_content)
        response_text = f"Memory logged successfully, boss. I have locked this into the core file array: *\"{memory_content}\"*."

    # --- INTERCEPT 6: FILE OPERATIONS MATRIX ---
    elif "list files" in cleaned_input or "show files" in cleaned_input:
        try:
            files_list = os.listdir(".")
            formatted_files = "\n".join([f"📁 {item}" if os.path.isdir(item) else f"📄 {item}" for item in files_list])
            response_text = f"Scanning active `ONIX` project directory, boss:\n\n{formatted_files}"
        except Exception as e:
            response_text = f"Failed to parse directory matrix: {e}"

    # --- MODULE 1: LIVE SEARCH INTERCEPT ---
    elif any(word in cleaned_input for word in ["search", "news", "weather", "latest", "who is", "what is the"]):
        with st.spinner("Scraping live indices..."):
            search_data = live_web_search(user_input)
            if search_data and client:
                try:
                    search_prompt = f"The user is asking a real-time question: '{user_input}'. Use this live web information to answer concisely as Onix: {search_data}"
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": search_prompt}],
                        model="llama-3.1-8b-instant",
                        temperature=0.4,
                    )
                    response_text = chat_completion.choices[0].message.content
                except Exception as e:
                    response_text = f"Search interpretation error: {e}"
            else:
                response_text = "I couldn't retrieve live data packets right now, boss."

    # Output responses and speak out loud
    if response_text:
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        speak_out_loud(response_text)
        st.rerun()

    # --- DEFAULT TO GROQ CLOUD FOR GENERAL INTELLIGENCE ---
    elif client:
        with st.chat_message("assistant"):
            with st.spinner("Streaming from Groq array..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_input}],
                        model="llama-3.1-8b-instant",
                        temperature=0.7,
                    )
                    response_text = chat_completion.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    speak_out_loud(response_text)
                except Exception as e:
                    st.error(f"Engine connection issue: {e}")