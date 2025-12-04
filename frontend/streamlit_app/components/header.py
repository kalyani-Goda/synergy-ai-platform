import streamlit as st

def display_header():
    """Display header with ADK badge"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-title">🎯 Synergy AI ADK</h1>', unsafe_allow_html=True)
        st.markdown('<div class="adk-badge">Powered by Google Agent Development Kit</div>', 
                   unsafe_allow_html=True)
        st.caption("Multi-Agent Productivity Platform")
    st.markdown("---")