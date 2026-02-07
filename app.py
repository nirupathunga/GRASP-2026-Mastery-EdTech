import streamlit as st
import requests
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cognify | AI Mastery", page_icon="🧠", layout="wide")

# Custom CSS for a better look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #2e77d0; color: white; }
    .topic-card { padding: 20px; border-radius: 15px; background-color: white; border: 1px solid #e1e4e8; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Cognify: AI-Powered Mastery")
st.write("Stop rote learning. Explain concepts in your own words to prove mastery.")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("Settings")
    backend_url = st.text_input("Backend URL", value="http://127.0.0.1:8000")
    st.divider()
    st.info("Ensure main.py is running in your other terminal.")

# --- STEP 1: SYLLABUS UPLOAD ---
st.subheader("1. Upload Syllabus")
uploaded_file = st.file_uploader("Upload your PDF (Biology, Physics, etc.)", type="pdf")

if uploaded_file and 'syllabus' not in st.session_state:
    if st.button("🚀 Generate Mastery Map"):
        with st.spinner("AI is analyzing syllabus & mapping Bloom's Taxonomy..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{backend_url}/upload-syllabus", files=files)
                
                if response.status_code == 200:
                    st.session_state['syllabus'] = response.json()
                    st.rerun()
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- STEP 2: MASTERY DASHBOARD ---
if 'syllabus' in st.session_state:
    st.divider()
    st.subheader("2. Your Mastery Dashboard")
    
    topics = st.session_state['syllabus'].get('topics', [])
    
    # Create a grid of topics
    cols = st.columns(3)
    for idx, topic in enumerate(topics):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="topic-card">
                    <h4>{topic['title']}</h4>
                    <p style="color: #666; font-size: 0.8em;">Level: {topic.get('level', 'Understand')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Audit: {topic['title']}", key=f"btn_{idx}"):
                st.session_state['active_topic'] = topic['title']

# --- STEP 3: VOICE LOGIC AUDIT ---
if 'active_topic' in st.session_state:
    st.divider()
    st.subheader(f"3. Voice Audit: {st.session_state['active_topic']}")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.write("Click the mic and explain the concept.")
        audio_value = st.audio_input("Record your explanation")
    
    if audio_value:
        with col_b:
            with st.spinner("AI is performing Semantic Gap Analysis..."):
                try:
                    payload = {"topic": st.session_state['active_topic']}
                    files = {"audio": ("audit.wav", audio_value.getvalue(), "audio/wav")}
                    
                    audit_res = requests.post(f"{backend_url}/test-understanding", data=payload, files=files)
                    
                    if audit_res.status_code == 200:
                        result = audit_res.json()
                        
                        # Display Results
                        score = result.get('score', 0)
                        status = "✅ Mastered" if score >= 80 else "🔍 Learning Gap"
                        
                        st.metric(label="Mastery Score", value=f"{score}%", delta=status)
                        st.write(f"**Feedback:** {result.get('feedback')}")
                        
                        if 're_teaching' in result:
                            st.warning(f"**Try this Analogy:** {result['re_teaching']}")
                    else:
                        st.error("Audit failed. Check backend logs.")
                except Exception as e:
                    st.error(f"Error: {e}")