import streamlit as st
from datetime import datetime

def init_session_state():
    """Initialize all session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M')}"
    if 'plans' not in st.session_state:
        st.session_state.plans = []
    
    # Mock Interview States
    if 'mock_state' not in st.session_state:
        st.session_state.mock_state = 'ready' # ready, interviewing, evaluating, finished
    if 'mock_session_id' not in st.session_state:
        st.session_state.mock_session_id = None
    if 'mock_history' not in st.session_state:
        st.session_state.mock_history = []
    if 'interview_context' not in st.session_state:
        st.session_state.interview_context = {}