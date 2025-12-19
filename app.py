import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page Configuration
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. Advanced Premium CSS (Jarvis Style)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    /* Animated Glowing Ring */
    .ring-container { display: flex; justify-content: center; padding: 20px; }
    .ring {
        width: 200px; height: 200px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00d2ff;
        box-shadow: 0 0 20px #00d2ff, inset 0 0 20px #00d2ff;
        animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    /* Modern Chat Bubbles */
    .user-bubble {
        background: linear-gradient(135deg, #222, #333);
        color: white; padding: 15px; border-radius: 20px 20px 0px 20px;
        margin: 10px; border-left: 4px solid #00d2ff; float: right; width: 70%;
    }
    .ai-bubble {
        background: linear-gradient(135deg, #00d2ff, #008fb3);
        color: black; padding: 15px; border-radius: 20px 20px 20px 0px;
        margin: 10px; font-weight: bold; float: left; width: 70%;
        box-shadow: 0 4px 15px rgba(0,210,255,0.3);
    }
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    """, unsafe_allow_html=True)

# 3. Branding & Title
st.markdown("<h1 style='text-align: center; color: #00d2ff; font-family: sans-serif;'>🎙️ SHANKAR AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>System Status: Online | Creator: Devesh Kumar</p>", unsafe_allow_html=True)

# 4. Core Logic
api_key = st.secrets.get("GEMINI_API_KEY")

if "history" not in st.session_state:
    st.session_state.history = []

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# 5. Chat Input
query = st.chat_input("Shankar AI को आदेश दें...")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    # Sabse stable URL ka upyog
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=10)
        if response.status_code == 200:
            ans = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ans})
            speak(ans)
        else:
            st.error("सर्वर थोड़ा व्यस्त है, कृपया दोबारा प्रयास करें।")
    except:
        st.error("इंटरनेट कनेक्शन चेक करें।")

# 6. Displaying Bubbles
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f'<div class="user-bubble">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
