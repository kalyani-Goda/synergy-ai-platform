import requests
import streamlit as st
import os

# Default to localhost, but allow env var override for Docker
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class APIClient:
    @staticmethod
    def get_health():
        try:
            return requests.get(f"{BACKEND_URL}/health", timeout=2).status_code == 200
        except:
            return False

    @staticmethod
    def generate_daily_plan(user_id, goals, stress_level, session_id=None):
        return requests.post(f"{BACKEND_URL}/api/daily-plan", json={
            "user_id": user_id,
            "goals": goals,
            "session_id": session_id,
            "stress_level": stress_level
        })

    @staticmethod
    def generate_interview_prep(user_id, role, company, description):
        return requests.post(f"{BACKEND_URL}/api/interview-prep", json={
            "user_id": user_id,
            "role": role,
            "company": company,
            "description": description
        })

    @staticmethod
    def generate_quiz(user_id, topic, notes, difficulty):
        return requests.post(f"{BACKEND_URL}/api/quiz", json={
            "user_id": user_id,
            "topic": topic,
            "notes": notes,
            "difficulty": difficulty
        })

    @staticmethod
    def search_jobs(user_id, role, level, experience, location):
        return requests.post(f"{BACKEND_URL}/api/job-search", json={
            "user_id": user_id,
            "role": role,
            "level": level,
            "experience": experience,
            "location": location
        })

    # Mock Interview Methods
    @staticmethod
    def start_mock_interview(user_id, role, company, topics):
        return requests.post(f"{BACKEND_URL}/api/mock-interview/start", json={
            "user_id": user_id,
            "role": role,
            "company": company,
            "common_topics": topics
        })

    @staticmethod
    def continue_mock_interview(user_id, session_id, user_response):
        return requests.post(f"{BACKEND_URL}/api/mock-interview/continue", json={
            "user_id": user_id,
            "session_id": session_id,
            "user_response": user_response
        })

    @staticmethod
    def evaluate_interview(user_id, session_id):
        return requests.post(f"{BACKEND_URL}/api/mock-interview/evaluate", json={
            "user_id": user_id,
            "session_id": session_id
        })

    @staticmethod
    def analyze_resume(user_id, resume_text, job_description):
        return requests.post(f"{BACKEND_URL}/api/resume-analyze", json={
            "user_id": user_id,
            "resume_text": resume_text,
            "job_description": job_description
        })
    
    @staticmethod
    def evaluate_output(user_prompt, ai_response):
        return requests.post(f"{BACKEND_URL}/api/evaluate", json={
            "user_prompt": user_prompt, 
            "ai_response": ai_response
        })

    @staticmethod
    def get_traces():
        try:
            return requests.get(f"{BACKEND_URL}/api/traces").json().get("traces", [])
        except:
            return []
        
api_client = APIClient()