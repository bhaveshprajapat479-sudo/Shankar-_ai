import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page Configuration
st.set_page_config(page_title="Shankar AI", layout="wide")

# 2. Advanced Animation & CSS
if "speaking" not in st.session_state: st.session_state.speaking = False
speed = "0.4s" if st.session_state.speaking else "1.5s"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; }}
    .ring-container {{ display: flex; justify-content: center; padding: 10px; }}
    .ring {{
        width: 150px; height: 150px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00d2ff;
        box-shadow: 0 0 20px #00d2ff; animation: spin {speed} linear infinite;
    }}
    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    .user-bubble {{ background: #222; color: white; padding: 12px; border-radius: 15px; margin: 10px; float: right; width: 75%; border-left: 4px solid #00d2ff; }}
    .ai-bubble {{ background: #00d2ff; color: black; padding: 12px; border-radius: 15px; margin: 10px; font-weight: bold; float: left; width: 75%; }}
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00d2ff;'>🎙️ SHANKAR AI</h1>", unsafe_allow_html=True)

# 3. Voice Logic (Name: Devesh included)
def speak(text):
    full_text = f"नमस्ते देवेश, {text}" if "history" in st.session_state and len(st.session_state.history) < 3 else text
    tts = gTTS(text=full_text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# 4. Core Interaction
api_key = st.secrets.get("GEMINI_API_KEY")
if "history" not in st.session_state: st.session_state.history = []

query = st.chat_input("Shankar AI को आदेश दें...")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.speaking = False
    
    # Corrected & Most Stable URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        res = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ans})
            st.session_state.speaking = True
            speak(ans)
            st.rerun()
        else:
            st.warning("गूगल सर्वर से कनेक्ट हो रहा है... कृपया दोबारा लिखें।")
    except:
        st.error("Connection error! Please check Internet.")

# 5. Display History
for chat in st.session_state.history:
    cls = "user-bubble" if chat["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="{cls}">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
