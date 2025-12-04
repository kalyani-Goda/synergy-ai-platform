import streamlit as st
from services.api_client import api_client

def render_sidebar():
    # Check backend connection
    if api_client.get_health():
        st.sidebar.success("✅ Backend Connected")
    else:
        st.sidebar.error("❌ Backend Offline")
    
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        st.text_input("User ID", value=st.session_state.user_id, disabled=True)
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Start")
        
        if st.button("🎯 Study Day Template"):
            st.session_state.template_goals = "Study Python for 3 hours, break every 45 minutes"
        
        if st.button("💼 Job Hunt Template"):
            st.session_state.template_goals = "Update resume, apply to 5 jobs, practice interviews"