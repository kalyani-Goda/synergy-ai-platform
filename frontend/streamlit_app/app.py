import streamlit as st
import os

# Set config MUST be the first Streamlit command
st.set_page_config(page_title="Synergy AI ADK", page_icon="🎯", layout="wide")

# Internal imports
from utils.session_state import init_session_state
from components.header import display_header
from components.sidebar import render_sidebar
from components.agent_cards import render_agent_dashboard
from pages import daily_plan, interview, quiz, job_search, history, observability

# Load CSS
def load_css():
    with open(os.path.join(os.path.dirname(__file__), "styles/custom.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    load_css()
    init_session_state()
    
    display_header()
    render_sidebar()
    render_agent_dashboard()
    st.markdown("---")
    
    # Tabs orchestration
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📅 Daily Plan", "💼 Interview", "🧠 Quiz", 
        "💼 Job Search", "📊 History", "🛠️ Observability"
    ])
    
    with tab1: daily_plan.show()
    with tab2: interview.show()
    with tab3: quiz.show()
    with tab4: job_search.show()
    with tab5: history.show()
    with tab6: observability.show()
if __name__ == "__main__":
    main()