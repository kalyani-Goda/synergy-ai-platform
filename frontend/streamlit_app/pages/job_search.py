import streamlit as st
from services.api_client import api_client
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def show():
    st.header("💼 Job Hub")
    tab_search, tab_resume = st.tabs(["🔍 Find Jobs", "📄 Resume Matcher (RAG)"])
    
    # --- TAB 1: JOB SEARCH ---
    with tab_search:
        if 'search_result' not in st.session_state: st.session_state.search_result = None
        if 'search_links' not in st.session_state: st.session_state.search_links = {}
        if 'search_query' not in st.session_state: st.session_state.search_query = ""

        with st.form("job_search_form"):
            col1, col2 = st.columns(2)
            with col1:
                role = st.text_input("Job Role", value="AI Engineer")
                level = st.selectbox("Level", ['Entry', 'Junior', 'Mid', 'Senior'], index=3)
            with col2:
                location = st.text_input("Location", value="Remote")
                exp = st.number_input("Years Experience", 0, 40, 2)
            submit = st.form_submit_button("Find Jobs", type="primary")

        if submit:
            with st.spinner("Searching..."):
                resp = api_client.search_jobs(st.session_state.user_id, role, level, exp, location)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.search_result = data.get("agent_response", "")
                    st.session_state.search_links = data.get("direct_links", {})
                    st.session_state.search_query = f"{level} {role} in {location}"
                else:
                    st.error(f"Error: {resp.text}")

        # Display Search Results
        if st.session_state.search_result:
            st.success("✅ Search complete!")
            st.markdown(st.session_state.search_result)
            
            if st.session_state.search_links:
                st.markdown("### 🔗 Quick Links")
                for site, url in st.session_state.search_links.items():
                    st.markdown(f"- [{site}]({url})")
            
            st.divider()
            if st.button("⚖️ Rate Search Quality"):
                with st.spinner("Evaluating..."):
                    e_resp = api_client.evaluate_output(
                        st.session_state.search_query, 
                        st.session_state.search_result
                    )
                    if e_resp.status_code == 200:
                        st.info("Evaluation Report")
                        st.markdown(e_resp.json().get("evaluation"))

    # --- TAB 2: RESUME ANALYSIS ---
    with tab_resume:
        st.subheader("📄 ATS Resume Analyzer")
        st.info("Upload your Resume (PDF) and paste a Job Description.")
        
        col_res, col_jd = st.columns(2)
        with col_res:
            uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        with col_jd:
            jd_text = st.text_area("Paste Job Description", height=200)

        # We don't need 'st.form' here since file_uploader behaves oddly in forms sometimes
        # We can just use a regular button since there are no results to "persist" outside a form loop yet
        if st.button("Analyze Match", type="primary"):
            if uploaded_file and jd_text:
                with st.spinner("Analyzing..."):
                    resume_text = extract_text_from_pdf(uploaded_file)
                    if resume_text:
                        resp = api_client.analyze_resume(st.session_state.user_id, resume_text, jd_text)
                        if resp.status_code == 200:
                            st.success("Analysis Complete!")
                            st.markdown("---")
                            st.markdown(resp.json().get("analysis", ""))
                        else:
                            st.error(f"Failed: {resp.text}")
            else:
                st.warning("Please upload both files.")