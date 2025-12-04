import streamlit as st
from services.api_client import api_client
from components.chat_interface import render_chat_messages, render_chat_input_area

def show():
    st.header("💼 Interview Hub")
    tab_plan, tab_mock = st.tabs(["📋 Preparation Plan", "🎤 Mock Interview"])
    
    with tab_plan:
        _render_prep_tab()
    with tab_mock:
        _render_mock_tab()

def _render_prep_tab():
    # Initialize state
    if 'interview_plan_result' not in st.session_state:
        st.session_state.interview_plan_result = None
    if 'interview_plan_input' not in st.session_state:
        st.session_state.interview_plan_input = ""

    # 1. Input Form
    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Target Role", key="prep_role")
            company = st.text_input("Target Company", key="prep_company")
        with col2:
            _ = st.selectbox("Experience", ["Entry", "Senior"], key="prep_exp")
        
        desc = st.text_area("Job Description", key="prep_desc")
        submit = st.form_submit_button("Prepare Interview", type="primary")

    # 2. Logic
    if submit and role:
        with st.spinner("Researching..."):
            resp = api_client.generate_interview_prep(st.session_state.user_id, role, company, desc)
            if resp.status_code == 200:
                st.session_state.interview_plan_result = resp.json().get("plan", "")
                st.session_state.interview_plan_input = f"Role: {role}, Company: {company}, Desc: {desc}"
            else:
                st.error("Failed to generate plan.")

    # 3. Display & Evaluate (Outside Form)
    if st.session_state.interview_plan_result:
        st.markdown(st.session_state.interview_plan_result)
        st.divider()
        if st.button("⚖️ Rate this Plan"):
            with st.spinner("Evaluating..."):
                e_resp = api_client.evaluate_output(
                    st.session_state.interview_plan_input, 
                    st.session_state.interview_plan_result
                )
                if e_resp.status_code == 200:
                    st.info("Evaluation Report")
                    st.markdown(e_resp.json().get("evaluation"))

def _render_mock_tab():
    state = st.session_state.mock_state
    
    if state == 'ready':
        with st.form("mock_start"):
            role = st.text_input("Role", key="mock_role")
            company = st.text_input("Company", key="mock_comp")
            topics = st.text_area("Topics", "Data Structures, System Design")
            if st.form_submit_button("Start Mock Interview") and role:
                with st.spinner("Initializing..."):
                    resp = api_client.start_mock_interview(st.session_state.user_id, role, company, topics.split(','))
                    if resp.status_code == 200:
                        res = resp.json()
                        st.session_state.mock_session_id = res.get("session_id")
                        st.session_state.mock_history = [{"role": "interviewer", "content": res.get("response")}]
                        st.session_state.interview_context = {"role": role, "company": company}
                        st.session_state.mock_state = 'interviewing'
                        st.rerun()

    elif state == 'interviewing':
        st.subheader(f"Mock Interview: {st.session_state.interview_context.get('role')}")
        render_chat_messages(st.session_state.mock_history)
        
        user_input, send_btn, end_btn = render_chat_input_area()
        
        if end_btn:
            st.session_state.mock_state = 'evaluating'
            st.rerun()
            
        if send_btn and user_input:
            st.session_state.mock_history.append({"role": "user", "content": user_input})
            del st.session_state["mock_user_input"] # Clear input
            
            with st.spinner("Thinking..."):
                resp = api_client.continue_mock_interview(st.session_state.user_id, st.session_state.mock_session_id, user_input)
                if resp.status_code == 200:
                    reply = resp.json().get("response", "")
                    st.session_state.mock_history.append({"role": "interviewer", "content": reply})
                    if "final question" in reply.lower(): 
                        st.session_state.mock_state = 'evaluating'
                    st.rerun()

    elif state == 'evaluating':
        st.info("Generating evaluation...")
        resp = api_client.evaluate_interview(st.session_state.user_id, st.session_state.mock_session_id)
        if resp.status_code == 200:
            st.session_state.mock_history.append({"role": "evaluation", "content": resp.json().get("summary")})
            st.session_state.mock_state = 'finished'
            st.rerun()
            
    elif state == 'finished':
        render_chat_messages(st.session_state.mock_history)
        if st.button("New Interview"):
            st.session_state.mock_state = 'ready'
            st.rerun()