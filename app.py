import streamlit as st
import requests
from gtts import gTTS
import base64
import io

# 1. Page & Animation Config
st.set_page_config(page_title="Shankar AI", layout="wide")

if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

# 2. Dynamic Animation CSS
# Jab AI bolega, animation speed 1.2s se 0.3s ho jayegi
anim_speed = "0.3s" if st.session_state.is_speaking else "1.2s"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000; }}
    .ring-container {{ display: flex; justify-content: center; padding: 20px; }}
    .ring {{
        width: 150px; height: 150px; border: 4px solid #111;
        border-radius: 50%; border-top: 4px solid #00d2ff;
        box-shadow: 0 0 20px #00d2ff;
        animation: spin {anim_speed} linear infinite;
    }}
    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    .user-bubble {{ background: #222; color: white; padding: 12px; border-radius: 15px; margin: 5px; float: right; width: 75%; border-left: 4px solid #00d2ff; }}
    .ai-bubble {{ background: #00d2ff; color: black; padding: 12px; border-radius: 15px; margin: 5px; font-weight: bold; float: left; width: 75%; }}
    </style>
    <div class="ring-container"><div class="ring"></div></div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #00d2ff;'>🎙️ SHANKAR AI</h1>", unsafe_allow_html=True)

# 3. Voice Output & Animation Trigger
def speak(text):
    try:
        st.session_state.is_speaking = True
        tts = gTTS(text=text, lang='hi')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        # Refresh to slow down animation after speaking (Optional)
    except: pass

# 4. Input & API Logic
api_key = st.secrets.get("GEMINI_API_KEY")
if "history" not in st.session_state: st.session_state.history = []

query = st.chat_input("Shankar AI को आदेश दें...")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.is_speaking = False # Reset animation for new query
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": query}]}]}, timeout=15)
        if response.status_code == 200:
            ans = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state.history.append({"role": "assistant", "content": ans})
            speak(ans)
            st.rerun() # Animation update ke liye
        else:
            st.error("सर्वर लोड नहीं ले पा रहा, दोबारा पूछें।")
    except:
        st.error("Connection Time Out!")

# 5. Display
for chat in st.session_state.history:
    style = "user-bubble" if chat["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="{style}">{chat["content"]}</div><div style="clear:both;"></div>', unsafe_allow_html=True)
