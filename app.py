import streamlit as st
import requests
from gtts import gTTS
import base64
import io
import time

# 1. Page Configuration
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. UI & Ring Animation
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
    .ai-bubble { background: #00d2ff; color: black; padding: 12px; border-radius: 15px; margin: 10px; font-weight: bold; width: 85%; }
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    <h1 style='text-align: center; color: #00d2ff;'>🎙️ SHANKAR AI</h1>
    """, unsafe_allow_html=True)

# 3. Mic System (Wapas Add Kar Diya Hai)
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="micBtn" style="background:#00d2ff; border:none; border-radius:50%; width:65px; height:65px; font-size:32px; cursor:pointer;">🎤</button>
        <p style="color:#00d2ff; margin-top:8px; font-family:sans-serif;">माइक दबाकर बोलें</p>
    </div>
    <script>
    const btn = document.getElementById('micBtn');
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    btn.onclick = () => { recognition.start(); btn.style.background = 'red'; };
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:set_widget_value', data: {id: 'shankar_chat', value: text}}, '*');
        btn.style.background = '#00d2ff';
    };
    </script>
    """, height=120)

# API Key (Direct input to avoid Secrets delay)
API_KEY = "AIzaSyCcO05rtWkhQlrqQRGs_VYsu_X2kcZdO0Y"

def speak(text):
    try:
        tts = gTTS(text=f"जी देवेश, {text}", lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

query = st.chat_input("यहाँ लिखें या माइक का उपयोग करें...", key="shankar_chat")

if query:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    success = False
    
    # Retry logic to handle "Busy" error
    for i in range(2):
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=25)
            if res.status_code == 200:
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.markdown(f'<div class="ai-bubble">{ans}</div>', unsafe_allow_html=True)
                speak(ans)
                success = True
                break
            else:
                time.sleep(2)
        except:
            continue
            
    if not success:
        st.warning("सर्वर थोड़ा सुस्त है, कृपया एक बार फिर 'Send' दबाएं।")
