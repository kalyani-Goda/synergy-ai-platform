import streamlit as st
from services.api_client import api_client

def show():
    st.header("🧠 Quiz Generator")
    
    if 'quiz_result' not in st.session_state:
        st.session_state.quiz_result = None
    if 'quiz_topic' not in st.session_state:
        st.session_state.quiz_topic = ""

    # 1. Form
    with st.form("quiz_form"):
        topic = st.text_input("Topic")
        notes = st.text_area("Notes")
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])
        submit = st.form_submit_button("Generate Quiz", type="primary")
        
    # 2. Logic
    if submit and topic:
        with st.spinner("Generating..."):
            resp = api_client.generate_quiz(st.session_state.user_id, topic, notes, difficulty)
            if resp.status_code == 200:
                st.session_state.quiz_result = resp.json().get("quiz", "")
                st.session_state.quiz_topic = f"Topic: {topic}, Level: {difficulty}"
            else:
                st.error("Quiz generation failed.")

    # 3. Display (Outside Form)
    if st.session_state.quiz_result:
        st.markdown(st.session_state.quiz_result)
        st.divider()
        if st.button("⚖️ Rate this Quiz"):
            with st.spinner("Evaluating quality..."):
                e_resp = api_client.evaluate_output(
                    st.session_state.quiz_topic, 
                    st.session_state.quiz_result
                )
                if e_resp.status_code == 200:
                    st.info("Evaluation Report")
                    st.markdown(e_resp.json().get("evaluation"))