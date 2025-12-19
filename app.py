import streamlit as st
import os
import requests
import json
from io import BytesIO
import tempfile
import base64

# --- Gemini API Key Configuration ---
# सुनिश्चित करें कि आपने Streamlit Secrets में GEMINI_API_KEY को सही तरीके से सेट किया है
if "GEMINI_API_KEY" not in st.secrets:
    st.error("कृपया Streamlit Secrets में GEMINI_API_KEY को सेट करें।")
    st.stop()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Shankar AI Voice Assistant", layout="centered")

st.title("🤖 Shankar AI Assistant (आपके लिए!)")
st.caption("✨ Voice Input और Output के साथ Gemini-pro:पर आधारित।")
st.markdown("निर्माता: **दिवेश कुमार**")
st.markdown("---")


# --- Function to call Gemini API ---
def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "config": {"temperature": 0.7}
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise exception for bad status codes
        
        result = response.json()
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "क्षमा करें, मुझे कोई प्रतिक्रिया नहीं मिली।"
            
    except requests.exceptions.RequestException as e:
        st.error(f"API कॉल में त्रुटि: {e}")
        return "API से कनेक्ट करने में समस्या आई।"

# --- Voice Output Function (Text-to-Speech) ---
def text_to_speech(text):
    # यह सिर्फ एक उदाहरण है। Text-to-Speech के लिए आपको Google Cloud TTS या किसी अन्य सेवा की
    # API की ज़रूरत होगी, जिसकी कुंजी (Key) भी Secrets में सेट करनी होगी।
    st.warning("वॉइस आउटपुट फ़ंक्शन अभी सक्रिय नहीं है। इसे सक्रिय करने के लिए अतिरिक्त TTS API की ज़रूरत होगी।")
    # For now, we will only display the text.
    pass

# --- Chat Interface Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Placeholder for Voice Input ---
st.info("वॉइस इनपुट के लिए, अपने फ़ोन के कीबोर्ड या ब्राउज़र में 'Mic' बटन का उपयोग करें।")

if prompt := st.chat_input("Shankar AI से बात करें..."):
    # 1. User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Shankar AI सोच रहा है..."):
            response = get_gemini_response(prompt)
            st.markdown(response)
        
        # 3. Voice Output (Optional/Placeholder)
        text_to_speech(response)
        
        # 4. Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})

                           
