import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="Shankar AI Pro Max", layout="centered", page_icon="🎤")

# Custom CSS for Premium Look & Buttons
st.markdown("""
    <style>
    .stTextInput > div > div > input { border-radius: 25px; padding: 12px; }
    .share-btn {
        background-color: #007bff; color: white; padding: 10px 20px;
        border-radius: 20px; text-decoration: none; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🔎 Shankar AI Pro Max")
st.markdown("निर्माता: **देवेश कुमार** | स्कूल: **MKVV** | कक्षा: **9th**")

# Input Section with Mic Mention
st.info("🎤 माइक इनपुट के लिए अपने कीबोर्ड का माइक इस्तेमाल करें।")
user_query = st.text_input("", placeholder="यहाँ बोलकर या लिखकर पूछें...")

# Share Button Logic
app_url = "https://shankar-ai-aqu8tgjid.streamlit.app/"
st.markdown(f'<a href="whatsapp://send?text=Check out my AI app: {app_url}" class="share-btn">📲 WhatsApp पर शेयर करें</a>', unsafe_allow_html=True)

# API Call
api_key = st.secrets["GEMINI_API_KEY"]

if user_query:
    with st.spinner('सोच रहा हूँ...'):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        response = requests.post(url, json={"contents": [{"parts": [{"text": user_query}]}]})
        if response.status_code == 200:
            st.success(response.json()['candidates'][0]['content']['parts'][0]['text'])
        else:
            st.error("API Key की समस्या है।")





