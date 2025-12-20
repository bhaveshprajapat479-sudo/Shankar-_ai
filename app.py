import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page Config
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. Animation & Look
if "speaking" not in st.session_state: st.session_state.speaking = False
speed = "0.4s" if st.session_state.speaking else "1.5s"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; color: #00d2ff; }}
    .ring-container {{ display: flex; justify-content: center; padding: 10px; }}
    .ring {{
        width: 150px; height: 150px; border: 4px solid #111;
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

# 3. Dedicated Mic (Fixed)
st.components.v1.html("""
    <div style="text-align: center;">
        <button id="micBtn" style="background:#00d2ff; border:none; border-radius:50%; width:70px; height:70px; font-size:35px; cursor:pointer;">🎤</button>
        <p style="color:#00d2ff; margin-top:10px; font-family:sans-serif;">माइक दबाकर बोलें</p>
    </div>
    <script>
    const btn = document.getElementById('micBtn');
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    btn.onclick = () => { recognition.start(); btn.style.background = 'red'; };
    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:set_widget_value', data: {id: 'chat_input', value: text}}, '*');
        btn.style.background = '#00d2ff';
    };
    </script>
    """, height=130)

# 4. API & Voice Core
api_key = st.secrets.get("GEMINI_API_KEY")
if "history" not in st.session_state: st.session_state.history = []

def speak(text):
    tts = gTTS(text=f"नमस्ते देवेश, {text}", lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# 5. Interaction
query = st.chat_input("यहाँ लिखें या माइक का उपयोग करें...", key="chat_input")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.speaking = False
    
    # 100% Correct URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ans})
            st.session_state.speaking = True
            speak(ans)
            st.rerun()
        else: st.warning("सिस्टम जाग रहा है... एक बार फिर कोशिश करें।")
    except: st.error("नेटवर्क की समस्या है।")

for chat in st.session_state.history:
    style = "user-bubble" if chat["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="{style}">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
