import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page & Professional Look
st.set_page_config(page_title="Jarvis AI", layout="wide")

# 2. Premium CSS (Jarvis Style)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00e5ff; }
    .stApp { background-color: #000000; }
    
    /* Glowing Jarvis Ring */
    .jarvis-container {
        display: flex; justify-content: center; align-items: center; padding: 20px;
    }
    .ring {
        width: 180px; height: 180px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00e5ff;
        box-shadow: 0 0 15px #00e5ff, inset 0 0 15px #00e5ff;
        animation: spin 1.5s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    /* Premium Chat Bubbles */
    .chat-container { display: flex; flex-direction: column; }
    .user-bubble {
        background: linear-gradient(135deg, #1e1e1e, #2a2a2a);
        color: #fff; padding: 12px 18px; border-radius: 20px 20px 0 20px;
        align-self: flex-end; margin: 8px; border: 1px solid #00e5ff;
        max-width: 70%; box-shadow: 2px 2px 10px rgba(0,229,255,0.2);
    }
    .ai-bubble {
        background: linear-gradient(135deg, #00e5ff, #0097a7);
        color: #000; padding: 12px 18px; border-radius: 20px 20px 20px 0;
        align-self: flex-start; margin: 8px; font-weight: 600;
        max-width: 70%; box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    </style>
    <div class="jarvis-container"><div class="ring"></div></div>
    """, unsafe_allow_html=True)

# 3. App Title & Info
st.markdown("<h1 style='text-align: center; color: #00e5ff;'>🎙️ J.A.R.V.I.S (Shankar AI)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>System Online | Creator: Devesh Kumar (MKVV)</p>", unsafe_allow_html=True)

# 4. Logic & API
api_key = st.secrets.get("GEMINI_API_KEY")

if "history" not in st.session_state:
    st.session_state.history = []

def speak(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    st.markdown(audio_html, unsafe_allow_html=True)

# 5. Chat Input (Search Bar at bottom)
user_input = st.chat_input("Jarvis को आदेश दें...")

if user_input:
    # Add to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Get response from Google API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": user_input}]}]})
        if res.status_code == 200:
            ai_ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ai_ans})
            speak(ai_ans) # Voice response
        else:
            st.error("Connection Error with Jarvis Core.")
    except:
        st.error("Jarvis is offline.")

# 6. Display Chat Bubbles
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f'<div class="user-bubble">{chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{chat["content"]}</div>', unsafe_allow_html=True)
