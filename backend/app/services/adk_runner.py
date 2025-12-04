"""
Synergy AI Runner Service
Orchestrates agent execution using Google ADK Runners.
"""
import uuid
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from google.genai import types

# Google ADK imports
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.plugins.logging_plugin import LoggingPlugin

# Application imports
from ..core.config import settings
from ..agents.workflows import (
    daily_workflow, 
    interview_workflow, 
    quiz_workflow, 
    simple_job_search
)
from ..agents.mock_interview import interactive_interviewer, interview_evaluator
from ..agents.resume_agent import resume_agent
from ..agents.judge_agent import judge_agent 

class SynergyAIRunner:
    """Runner for Synergy AI agents"""
    
    def __init__(self):
        # Initialize Core Services
        # Note: We use the DATABASE_URL from settings
        self.session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)
        self.memory_service = InMemoryMemoryService()
        self.app_name = "synergy_ai_platform"
        
        # Stress level mapping
        self.stress_levels = {
            0: "RELAXED", 
            1: "STRESSED", 
            2: "ANXIOUS", 
            3: "OVERWHELMED"
        }

    def _get_runner(self, agent) -> Runner:
        """Helper to instantiate a Runner for a specific agent/workflow"""
        return Runner(
            agent=agent,
            app_name=self.app_name,
            session_service=self.session_service,
            memory_service=self.memory_service,
            plugins=[LoggingPlugin()]
        )
    
    async def _ensure_session(self, user_id: str, session_id: str):
        """Helper to ensure a session exists"""
        try:
            await self.session_service.create_session(
                app_name=self.app_name, 
                user_id=user_id, 
                session_id=session_id
            )
        except Exception:
            # Session likely exists, which is fine
            pass

    # =========================================================================
    # 1. DAILY PLANNER WORKFLOW
    # =========================================================================
    async def run_daily_plan(self, user_id: str, goals: str, session_id: str = None, stress_level: int = 1) -> Dict:
        """Run daily planning workflow"""
        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        await self._ensure_session(user_id, session_id)
        
        stress_text = self.stress_levels.get(stress_level, "STRESSED")
        
        try:
            # Create message
            message = types.Content(
                role="user",
                parts=[types.Part(text=f"Create a daily plan for these goals: {goals} and also consider my stress level: {stress_text}")]
            )
            
            # Initialize Runner with the Daily Workflow
            runner = self._get_runner(daily_workflow)
            
            final_event = None
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_event = event
            
            if final_event:
                response_text = final_event.content.parts[0].text

                self.log_trace("DailyWorkflow", goals, response_text)
                
                return {
                    "success": True,
                    "session_id": session_id,
                    "plan": response_text,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
            return {"success": False, "error": "No response generated"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 2. INTERVIEW PREP WORKFLOW (Plan Only)
    # =========================================================================
    async def run_interview_prep(self, user_id: str, role: str, company: str, description: str = None) -> Dict:
        """Run interview preparation workflow"""
        session_id = f"interview_{uuid.uuid4().hex[:8]}"
        await self._ensure_session(user_id, session_id)
        
        try:
            prompt = f"Prepare for {role} interview at {company}"
            if description:
                prompt += f"\nJob Description: {description}"
            
            message = types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
            
            runner = self._get_runner(interview_workflow)
            
            final_event = None
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_event = event
            
            if final_event:
                response_text = final_event.content.parts[0].text
                self.log_trace("InterviewWorkflow", prompt, response_text)
                return {
                    "success": True,
                    "session_id": session_id,
                    "plan": response_text,
                    "role": role,
                    "company": company,
                    "timestamp": datetime.now().isoformat()
                }
            return {"success": False, "error": "No response generated"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 3. QUIZ WORKFLOW
    # =========================================================================
    async def run_quiz_generation(self, user_id: str, topic: str, notes: str = "", difficulty: str = "medium") -> Dict:
        """Run quiz generation workflow"""
        session_id = f"quiz_{uuid.uuid4().hex[:8]}"
        await self._ensure_session(user_id, session_id)
        
        try:
            prompt = (
                f"topic: {topic}\n"
                f"notes: {notes}\n"
                f"difficulty: {difficulty}"
            )
            
            message = types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
            
            runner = self._get_runner(quiz_workflow)
            
            final_event = None
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_event = event
            
            if final_event:
                response_text = final_event.content.parts[0].text

                self.log_trace("QuizWorkflow", prompt, response_text)

                return {
                    "success": True,
                    "session_id": session_id,
                    "quiz": response_text,
                    "topic": topic,
                    "difficulty": difficulty,
                    "timestamp": datetime.now().isoformat()
                }
            return {"success": False, "error": "No response generated"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 4. MOCK INTERVIEW (Interactive State Machine)
    # =========================================================================
    async def start_mock_interview(self, user_id: str, role: str, company: str, common_topics: List[str]) -> Dict:
        """Starts a new interactive session and sets initial context."""
        session_id = f"mock_{uuid.uuid4().hex[:8]}"
        await self._ensure_session(user_id, session_id)
        
        # We need a dedicated runner for the interactive agent
        runner = self._get_runner(interactive_interviewer)
        
        initial_context_message = (
            f"START INTERVIEW for Role: {role}, Company: {company}. "
            f"Topics for context: {', '.join(common_topics)}"
        )
        
        initial_message = types.Content(
            role="user",
            parts=[types.Part(text=initial_context_message)]
        )
        
        final_event = None
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=initial_message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_event = event

        if final_event and final_event.content and final_event.content.parts:
            return {
                "success": True,
                "session_id": session_id,
                "response": final_event.content.parts[0].text
            }
        return {"success": False, "error": "Failed to initialize interview"}

    async def continue_mock_interview(self, user_id: str, session_id: str, user_response: str) -> Dict:
        """Sends user response and gets the next question."""
        # Re-instantiate runner for the same session
        runner = self._get_runner(interactive_interviewer)
        
        message = types.Content(
            role="user",
            parts=[types.Part(text=user_response)]
        )
        
        final_event = None
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_event = event
        
        if final_event and final_event.content and final_event.content.parts:
            return {
                "success": True,
                "session_id": session_id,
                "response": final_event.content.parts[0].text
            }
        return {"success": False, "error": "Session error or completion"}

    async def evaluate_interview(self, user_id: str, session_id: str) -> Dict:
        """Evaluates the entire session history using the EvaluatorAgent."""
        # Use the Evaluator Agent here
        runner = self._get_runner(interview_evaluator)
        
        message = types.Content(
            role="user",
            parts=[types.Part(text="Please generate the final evaluation and summary based on the conversation history.")]
        )
        
        final_event = None
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_event = event
        
        if final_event and final_event.content and final_event.content.parts:
            return {
                "success": True,
                "session_id": session_id,
                "summary": final_event.content.parts[0].text
            }
        return {"success": False, "error": "Evaluation failed or session not found"}

    # =========================================================================
    # 5. JOB SEARCH WORKFLOW
    # =========================================================================
    async def quick_job_search(self, user_id: str, role: str, level: str, experience: int, location: str = "") -> Dict:
        """Quick job search using Google"""
        session_id = f"quick_{uuid.uuid4().hex[:8]}"
        await self._ensure_session(user_id, session_id)
        
        try:
            prompt = f"""
            Find {level} level {role} jobs in {location} who already contains the {experience} years of previous experience.
            
            Search on:
            - LinkedIn
            - Indeed
            - Glassdoor
            - Naukri (if location is in India)
            
            Return specific job listings with links.
            """
            
            message = types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
            
            runner = self._get_runner(simple_job_search)
            
            final_response = None
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_response = event.content.parts[0].text

                    self.log_trace("JobSearchWorkflow", prompt, final_response)

            # Helper to generate example links locally (same as your original logic)
            role_slug = role.replace(' ', '+')
            location_slug = location.replace(' ', '+') if location else ""
            
            example_links = {
                "LinkedIn": f"https://linkedin.com/jobs/search/?keywords={role_slug}&location={location_slug}",
                "Indeed": f"https://indeed.com/q-{role.replace(' ', '-')}" + (f"-{location.replace(' ', '-')}" if location else "") + "-jobs.html",
                "Glassdoor": f"https://glassdoor.com/Job/{role.replace(' ', '-')}-jobs.htm",
                "Naukri": f"https://naukri.com/{role.replace(' ', '-')}-jobs" + (f"-in-{location.replace(' ', '-')}" if location else "")
            }
            
            return {
                "success": True,
                "session_id": session_id,
                "agent_response": final_response,
                "direct_links": example_links,
                "search_tips": [
                    f"Search: '{role} {level} {location}'",
                    "Filter by: Date posted (past 24 hours)",
                    "Set up job alerts"
                ],
                "timestamp": datetime.now().isoformat()
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    # =========================================================================
    # 6. RESUME ANALYSIS WORKFLOW
    # =========================================================================
    async def run_resume_analysis(self, user_id: str, resume_text: str, jd: str) -> Dict:
        """Run ATS Resume Analysis"""
        session_id = f"resume_{uuid.uuid4().hex[:8]}"
        await self._ensure_session(user_id, session_id)
        
        prompt = f"RESUME TEXT:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd}"
        
        message = types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
        
        runner = self._get_runner(resume_agent)
        
        final_text = ""
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=message):
            if event.is_final_response() and event.content:
                final_text = event.content.parts[0].text
                
        # Optional: Log this for observability
        # self.log_trace("ResumeAgent", prompt, final_text)
        
        return {
            "success": True, 
            "analysis": final_text,
            "session_id": session_id
        }
    
    def log_trace(self, agent_name: str, input_text: str, output_text: str):
        """Simple Observability: Log agent traces to a JSONL file"""
        trace_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "input": input_text[:200] + "...", # Truncate for readability
            "output": output_text,
            "status": "success"
        }
        
        # Write to the shared data volume so frontend can read it
        with open("/app/data/agent_traces.jsonl", "a") as f:
            f.write(json.dumps(trace_entry) + "\n")

    async def run_quality_check(self, user_prompt: str, ai_response: str) -> Dict:
        """Run LLM-as-a-Judge Evaluation"""
        session_id = f"eval_{uuid.uuid4().hex[:8]}"
        # Ensure session exists
        try:
            await self.session_service.create_session(
                app_name=self.app_name, 
                user_id="evaluator", 
                session_id=session_id
            )
        except Exception:
            pass
        
        message = types.Content(
            role="user",
            parts=[types.Part(text=f"User Prompt: {user_prompt}\nAI Response: {ai_response}")]
        )
        
        runner = self._get_runner(judge_agent)
        
        final_text = ""
        # FIX: Use keyword arguments (user_id=..., session_id=..., new_message=...)
        async for event in runner.run_async(
            user_id="evaluator", 
            session_id=session_id, 
            new_message=message
        ):
            if event.is_final_response() and event.content:
                final_text = event.content.parts[0].text
                
        return {"success": True, "evaluation": final_text}