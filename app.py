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

# 2. Universal Dark Theme & Reset Constraints
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
    /* Full bleed canvas restyling to lock dark mode elements */
    .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainBlockContainer"],
    .main,
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"] {
        background-color: #0e1117 !important;
    }

    /* Remove layout background masks */
    div[class^="st-emotion-cache"] {
        background-color: transparent !important;
    }

    /* Minimalist Ambient Particle System */
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
        background: rgba(255, 255, 255, 0.1);
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

# 3. Dynamic Shadow DOM Engine Injection (Applies smooth curves & the white circle button)
st.components.v1.html(
    """
    <script>
    function buildGeminiLayout() {
        const rootDoc = window.parent.document;
        
        // 1. Force the prompt text container box into smooth pill-shaped curves
        const inputContainers = rootDoc.querySelectorAll('[data-testid="stChatInputContainer"]');
        inputContainers.forEach(container => {
            container.style.borderRadius = '32px';
            container.style.backgroundColor = '#1a1f2c';
            container.style.border = '1px solid rgba(255, 255, 255, 0.08)';
            container.style.padding = '6px 16px';
            container.style.display = 'flex';
            container.style.alignItems = 'center';
        });

        // 2. Strip background fills from text entry blocks
        const inputs = rootDoc.querySelectorAll('[data-testid="stChatInputContainer"] textarea');
        inputs.forEach(text => {
            text.style.backgroundColor = 'transparent';
            text.style.color = '#f0f2f6';
        });

        // 3. Transform the submit button to a clean white circle container
        const submitButtons = rootDoc.querySelectorAll('button[data-testid="stChatInputSubmitButton"]');
        submitButtons.forEach(button => {
            button.style.backgroundColor = '#ffffff'; // Crisp white circle backdrop
            button.style.borderRadius = '50%';
            button.style.width = '32px';
            button.style.height = '32px';
            button.style.minWidth = '32px';
            button.style.display = 'flex';
            button.style.alignItems = 'center';
            button.style.justifyContent = 'center';
            button.style.border = 'none';
            button.style.padding = '0';
            button.style.marginRight = '2px';
            
            // Re-render internal SVG arrow cleanly into solid blue inside the circle
            const svgElements = button.querySelectorAll('svg');
            svgElements.forEach(svg => {
                svg.style.setProperty('fill', '#1a73e8', 'important');
                svg.style.setProperty('color', '#1a73e8', 'important');
                svg.style.setProperty('stroke', '#1a73e8', 'important');
                svg.style.setProperty('filter', 'none', 'important');
                svg.style.width = '16px';
                svg.style.height = '16px';
                
                const paths = svg.querySelectorAll('path');
                paths.forEach(path => {
                    path.style.setProperty('fill', '#1a73e8', 'important');
                    path.style.setProperty('stroke', '#1a73e8', 'important');
                });
            });
        });
    }

    // Run adjustments immediately and fire a continuous layout checker loop
    setTimeout(buildGeminiLayout, 200);
    setInterval(buildGeminiLayout, 400);
    </script>
    """,
    height=0,
    width=0
)

# 4. Tracking First-Time Page Load Animation State
if "animated" not in st.session_state:
    st.session_state.animated = False

# 5. Loading Animation Sequence
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

# 6. Secure API Key Retrieval
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("Authentication Missing. System offline.")
    st.stop()

client = Groq(api_key=api_key)

# 7. Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 8. Render Chat Logs Instantly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. Input Box Pipeline
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