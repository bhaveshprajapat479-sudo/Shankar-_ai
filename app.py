import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page Config
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. Advanced CSS & Ring
if "speaking" not in st.session_state: st.session_state.speaking = False
speed = "0.4s" if st.session_state.speaking else "1.5s"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #00d2ff; }}
    .ring-container {{ display: flex; justify-content: center; padding: 10px; }}
    .ring {{
        width: 140px; height: 140px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00d2ff;
        box-shadow: 0 0 20px #00d2ff; animation: spin {speed} linear infinite;
    }}
    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    .user-bubble {{ background: #222; color: white; padding: 12px; border-radius: 15px; margin: 10px; float: right; width: 80%; border-left: 4px solid #00d2ff; }}
    .ai-bubble {{ background: #00d2ff; color: black; padding: 12px; border-radius: 15px; margin: 10px; font-weight: bold; float: left; width: 80%; }}
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00d2ff;'>🎙️ SHANKAR AI</h1>", unsafe_allow_html=True)

# 3. Mic Integration
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="micBtn" style="background:#00d2ff; border:none; border-radius:50%; width:60px; height:60px; font-size:30px; cursor:pointer;">🎤</button>
        <p style="color:#00d2ff; margin-top:5px; font-family:sans-serif;">माइक दबाकर बोलें</p>
    </div>
    <script>
    const btn = document.getElementById('micBtn');
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    btn.onclick = () => { recognition.start(); btn.style.background = 'red'; };
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:set_widget_value', data: {id: 'chat_box', value: text}}, '*');
        btn.style.background = '#00d2ff';
    };
    </script>
    """, height=110)

# 4. Core Logic
api_key = st.secrets["GEMINI_API_KEY"]
if "history" not in st.session_state: st.session_state.history = []

def speak(text):
    tts = gTTS(text=f"जी देवेश, {text}", lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# Input
query = st.chat_input("यहाँ लिखें या माइक दबाएं...", key="chat_box")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.speaking = False
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": query}]}]}
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ans})
            st.session_state.speaking = True
            speak(ans)
            st.rerun()
        else: st.error("सर्वर से संपर्क नहीं हो पाया।")
    except: st.error("Network issue!")

# History Display
for chat in st.session_state.history:
    cls = "user-bubble" if chat["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="{cls}">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
