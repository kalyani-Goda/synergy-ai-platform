import streamlit as st
from datetime import datetime
from services.api_client import api_client

def show():
    st.header("🛠️ Agent Observability (Traces)")
    if st.button("Refresh Traces"):
        traces = api_client.get_traces()
        for trace in reversed(traces): # Show newest first
                with st.expander(f"{trace['timestamp']} - {trace['agent']}"):
                    st.json(trace)