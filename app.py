import streamlit as st
import requests
from gtts import gTTS
import base64
import io
import time

# 1. Page Config
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. Advanced Animation & UI
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

# 3. Mic Integration (Best for Mobile)
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
        window.parent.postMessage({type: 'streamlit:set_widget_value', data: {id: 'final_box', value: text}}, '*');
        btn.style.background = '#00d2ff';
    };
    </script>
    """, height=120)

# 4. API Core with Auto-Retry Logic
api_key = st.secrets.get("GEMINI_API_KEY")
if "history" not in st.session_state: st.session_state.history = []

def speak(text):
    full_msg = f"जी देवेश, {text}" if len(st.session_state.history) <= 2 else text
    try:
        tts = gTTS(text=full_msg, lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

query = st.chat_input("शंकर आपकी सेवा में तैयार है...", key="final_box")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.speaking = False
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Logic: It will try 3 times before showing an error
    for attempt in range(3):
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=30)
            if res.status_code == 200:
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.history.append({"role": "assistant", "content": ans})
                st.session_state.speaking = True
                speak(ans)
                st.rerun()
                break
            else:
                time.sleep(1) # Wait for 1 second and try again
        except:
            if attempt == 2:
                st.error("नेटवर्क बहुत धीमा है। कृपया अपना इंटरनेट कनेक्शन चेक करें।")

for chat in st.session_state.history:
    cls = "user-bubble" if chat["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="{cls}">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
