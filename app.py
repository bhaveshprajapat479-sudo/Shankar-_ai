import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page Config
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. UI & Bubble Styling
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00d2ff; }
    .ring-container { display: flex; justify-content: center; padding: 10px; }
    .ring {
        width: 150px; height: 150px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00d2ff;
        box-shadow: 0 0 20px #00d2ff; animation: spin 1s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .bubble { 
        background: #00d2ff; color: black; padding: 15px; 
        border-radius: 20px 20px 20px 0px; margin: 10px 0; 
        font-weight: bold; font-size: 18px; width: fit-content; max-width: 80%;
        box-shadow: 4px 4px 10px rgba(0,210,255,0.3);
    }
    .user-msg { color: #00d2ff; font-style: italic; margin-bottom: 5px; }
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    <h1 style='text-align: center; color: #00d2ff;'>🎙️ SHANKAR AI</h1>
    """, unsafe_allow_html=True)

# 3. Mic Integration
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="micBtn" style="background:#00d2ff; border:none; border-radius:50%; width:70px; height:70px; font-size:32px; cursor:pointer;">🎤</button>
        <p style="color:#00d2ff; margin-top:10px; font-family:sans-serif; font-weight:bold;">माइक दबाकर बोलें</p>
    </div>
    <script>
    const btn = document.getElementById('micBtn');
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    btn.onclick = () => { recognition.start(); btn.style.background = 'red'; };
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:set_widget_value', data: {id: 'shankar_final', value: text}}, '*');
        btn.style.background = '#00d2ff';
    };
    </script>
    """, height=130)

# API Core (Using your key directly)
API_KEY = "AIzaSyCcO05rtWkhQlrqQRGs_VYsu_X2kcZdO0Y"

def speak(text):
    try:
        tts = gTTS(text=f"जी देवेश, {text}", lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

query = st.chat_input("यहाँ लिखें या माइक का उपयोग करें...", key="shankar_final")

if query:
    st.markdown(f"<div class='user-msg'>आप: {query}</div>", unsafe_allow_html=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.markdown(f"<div class='bubble'>{ans}</div>", unsafe_allow_html=True)
            speak(ans)
        else:
            st.error("गूगल का मुफ्त सर्वर अभी व्यस्त है। कृपया 2 सेकंड बाद दोबारा 'Send' दबाएं।")
    except:
        st.error("कनेक्शन में समस्या।")
