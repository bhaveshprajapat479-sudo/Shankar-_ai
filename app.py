import streamlit as st
import requests

# Page Config
st.set_page_config(page_title="Shankar AI Pro Max", layout="centered", page_icon="🔎")

# Header Section
st.title("🔎 Shankar AI Pro Max")
st.markdown("निर्माता: **देवेश कुमार** | स्कूल: **MKVV** | कक्षा: **9th**")

# Get API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# Input Area
user_query = st.text_input("अपना सवाल यहाँ लिखें:", placeholder="पूछें...")

# AI को सवाल भेजने वाला बटन
submit_button = st.button("🚀 सवाल भेजें")

if submit_button and user_query:
    if not api_key:
        st.error("API Key नहीं मिली! कृपया Secrets चेक करें।")
    else:
        with st.spinner('एआई सोच रहा हूँ...'):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            try:
                response = requests.post(url, json={"contents": [{"parts": [{"text": user_query}]}]})
                if response.status_code == 200:
                    st.success(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"सर्वर की समस्या (Error {response.status_code})। कृपया थोड़ी देर बाद कोशिश करें।")
            except:
                st.error("नेटवर्क की समस्या है।")
