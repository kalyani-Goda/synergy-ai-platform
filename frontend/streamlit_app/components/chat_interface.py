import streamlit as st

def render_chat_messages(history):
    """Renders the chat history"""
    for message in history:
        if message["role"] == "interviewer":
            st.info(f"**Interviewer:** {message['content']}")
        elif message["role"] == "user":
            st.success(f"**You:** {message['content']}")
        elif message["role"] == "evaluation":
            st.markdown("### 📋 Final Impression and Feedback")
            st.markdown("---")
            st.markdown(message['content'])

def render_chat_input_area():
    """Renders input area and returns the values"""
    user_input = st.text_area("Your Answer", height=100, key="mock_user_input")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        send = st.button("Submit Answer", type="primary", key="send_ans_btn")
    with col2:
        end = st.button("End Interview", type="secondary", key="end_int_btn")
        
    return user_input, send, end