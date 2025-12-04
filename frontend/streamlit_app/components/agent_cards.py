import streamlit as st

def render_agent_dashboard():
    """Display agent dashboard"""
    st.header("🤖 Active Agents")
    cols = st.columns(3)
    
    agents = [
        {"name": "StudyAgent", "emoji": "📚", "desc": "Study planning"},
        {"name": "JobSearchAgent", "emoji": "💼", "desc": "Career planning"},
        {"name": "WellnessAgent", "emoji": "🌿", "desc": "Wellness advice"},
        {"name": "InterviewAgent", "emoji": "🎤", "desc": "Interview prep"},
        {"name": "QuizAgent", "emoji": "🧠", "desc": "Quiz generation"},
        {"name": "PlannerAgent", "emoji": "📅", "desc": "Schedule planning"}
    ]
    
    for idx, agent in enumerate(agents):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class="agent-card">
                    <h4>{agent['emoji']} {agent['name']}</h4>
                    <p>{agent['desc']}</p>
                </div>
                """, unsafe_allow_html=True)