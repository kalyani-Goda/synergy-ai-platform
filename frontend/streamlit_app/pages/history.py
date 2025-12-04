import streamlit as st

def show():
    st.header("📊 History")
    if not st.session_state.plans:
        st.info("No plans generated yet.")
        return
    
    for i, plan in enumerate(st.session_state.plans):
        with st.expander(f"Plan {i+1} - {plan['type']} - {plan['timestamp'][:19]}"):
            st.markdown(plan['content'])