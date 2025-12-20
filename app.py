import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# Page Config
st.set_page_config(page_title="Shankar AI", layout="wide")

# UI & Animation
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

# Directly using your key from the screenshot to ensure it works
API_KEY = "AIzaSyCcO05rtWkhQlrqQRGs_VYsu_X2kcZdO0Y"

def speak(text):
    try:
        tts = gTTS(text=f"जी देवेश, {text}", lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

query = st.chat_input("शंकर आपकी सेवा में तैयार है...")

if query:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.markdown(f'<div class="ai-bubble">{ans}</div>', unsafe_allow_html=True)
            speak(ans)
        else:
            st.error("गूगल सर्वर अभी बिजी है, कृपया 10 सेकंड बाद दोबारा कोशिश करें।")
    except:
        st.error("कनेक्शन फेल! कृपया नेट चेक करें।")
