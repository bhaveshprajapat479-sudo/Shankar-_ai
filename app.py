import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Shankar AI Pro", layout="centered", page_icon="🔎")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput > div > div > input {
        border-radius: 24px;
        padding: 12px 20px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 1px 6px rgba(32,33,36,0.28);
        font-size: 18px;
    }
    .stTextInput > div > div > input:focus {
        box-shadow: 0 1px 6px rgba(32,33,36,0.35);
        border: 1px solid #dfe1e5;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #70757a;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e8eaed;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; color: #202124; font-size: 50px;'>Shankar AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #70757a;'>निर्माता: <b>देवेश कुमार</b> | स्कूल: <b>MKVV</b> | कक्षा: <b>9th</b></p>", unsafe_allow_html=True)

# API Key from Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("API Key नहीं मिली! कृपया Streamlit Secrets चेक करें।")
    st.stop()

def get_pro_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: कृपया अपनी API Key चेक करें।"
    except:
        return "कलेक्शन में समस्या आ रही है।"

# Search Input Area
user_query = st.text_input("", placeholder="Shankar AI Pro से कुछ भी पूछें...")

if user_query:
    with st.spinner('खोज रहा हूँ...'):
        result = get_pro_response(user_query)
        st.markdown(f"<div style='background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #dadce0;'>{result}</div>", unsafe_allow_html=True)

# Chat Style Footer
st.markdown("""
    <div class="footer">
        ✨ Powered by Gemini Pro | Developed with ❤️ by Devesh Kumar
    </div>
    """, unsafe_allow_html=True)
