import streamlit as st
from datetime import datetime
from services.api_client import api_client

def show():
    st.header("📅 Daily Planning")
    
    # Initialize session state for the current plan if it doesn't exist
    # We use this to persist the plan so we can show it outside the form
    if 'current_daily_plan' not in st.session_state:
        st.session_state.current_daily_plan = None
    if 'current_daily_goals' not in st.session_state:
        st.session_state.current_daily_goals = ""

    # Pre-fill from sidebar template if clicked
    default_goals = getattr(st.session_state, 'template_goals', "")
    
    # --- 1. THE INPUT FORM ---
    with st.form("daily_plan_form"):
        goals = st.text_area("Your Goals", value=default_goals, height=100)
        col1, col2 = st.columns(2)
        with col1:
            stress_level = st.slider("Stress Level", 1, 3, 2)
        with col2:
            session_id = st.text_input("Session ID (optional)")
        
        # This is the ONLY button allowed inside the form
        submitted = st.form_submit_button("Generate Plan", type="primary")
    
    # --- 2. HANDLE SUBMISSION ---
    if submitted and goals:
        with st.spinner("🤖 ADK agents are collaborating..."):
            try:
                response = api_client.generate_daily_plan(
                    st.session_state.user_id, goals, stress_level, session_id
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Store in History
                    st.session_state.plans.append({
                        "type": "daily",
                        "content": result.get("plan", ""),
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Store in Session State for immediate display
                    st.session_state.current_daily_plan = result.get("plan", "")
                    st.session_state.current_daily_goals = goals # Save goals for evaluation
                    
                    st.success("✅ Plan generated!")
                    
                else:
                    st.error(f"Failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # --- 3. DISPLAY RESULTS & EVALUATION (OUTSIDE THE FORM) ---
    # This block runs if we just submitted OR if we already have a plan in memory
    if st.session_state.current_daily_plan:
        st.markdown("### 🎯 Your Daily Plan")
        st.markdown(st.session_state.current_daily_plan)
        
        st.divider()
        st.subheader("🛠️ Quality Check")
        
        # Now we can use st.button because we are outside the form!
        if st.button("⚖️ Rate this AI Output (LLM-as-a-Judge)"):
            with st.spinner("Judge Agent is evaluating..."):
                try:
                    eval_resp = api_client.evaluate_output(
                        st.session_state.current_daily_goals, 
                        st.session_state.current_daily_plan
                    )
                    
                    if eval_resp.status_code == 200:
                        st.info("Evaluation Report")
                        st.markdown(eval_resp.json().get("evaluation"))
                        st.balloons()
                    else:
                        st.error("Evaluation failed.")
                except Exception as e:
                    st.error(f"Evaluation connection error: {e}")