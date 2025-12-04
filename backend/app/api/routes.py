"""
API Routes for Synergy AI Platform
"""
import json
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List

# Import Pydantic Models
from ..models.requests import (
    DailyPlanRequest, 
    InterviewRequest, 
    QuizRequest, 
    JobSearchRequest,
    MockStartRequest, 
    MockContinueRequest, 
    MockEvaluateRequest,
    ResumeAnalysisRequest,
    EvalRequest
)

# Import Service
from ..services.adk_runner import SynergyAIRunner
from ..models.requests import ResumeAnalysisRequest # Add this to imports

# Initialize Router
router = APIRouter()

# Initialize Runner
# In a highly concurrent production env, you might use Depends() for dependency injection,
# but for this architecture, instantiating it here is efficient.
runner = SynergyAIRunner()

# =========================================================================
# 📅 DAILY PLANNER ROUTES
# =========================================================================
@router.post("/daily-plan")
async def create_daily_plan(request: DailyPlanRequest):
    """Create daily plan using ADK agents"""
    try:
        result = await runner.run_daily_plan(
            user_id=request.user_id,
            goals=request.goals,
            session_id=request.session_id,
            stress_level=request.stress_level
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# 💼 INTERVIEW PREP ROUTES (PLANNING)
# =========================================================================
@router.post("/interview-prep")
async def create_interview_prep(request: InterviewRequest):
    """Create interview preparation using ADK agents"""
    try:
        result = await runner.run_interview_prep(
            user_id=request.user_id,
            role=request.role,
            company=request.company,
            description=request.description
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# 🧠 QUIZ ROUTES
# =========================================================================
@router.post("/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate quiz using ADK agents"""
    try:
        result = await runner.run_quiz_generation(
            user_id=request.user_id,
            topic=request.topic,
            notes=request.notes,
            difficulty=request.difficulty
        )
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# 🔍 JOB SEARCH ROUTES
# =========================================================================
@router.post("/job-search")
async def run_job_search(request: JobSearchRequest):
    """Run JobSearchAgent for finding relevant job listings."""
    try:
        result = await runner.quick_job_search(
            user_id=request.user_id,
            role=request.role,
            level=request.level,
            experience=request.experience, 
            location=request.location
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Job search failed"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# 🎤 MOCK INTERVIEW ROUTES (INTERACTIVE)
# =========================================================================
@router.post("/mock-interview/start")
async def start_mock_interview(request: MockStartRequest):
    """Starts a new interactive mock interview session."""
    try:
        result = await runner.start_mock_interview(
            user_id=request.user_id,
            role=request.role,
            company=request.company,
            common_topics=request.common_topics
        )
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to start interview"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mock-interview/continue")
async def continue_mock_interview(request: MockContinueRequest):
    """Sends a user response to an ongoing session and gets the next question."""
    try:
        result = await runner.continue_mock_interview(
            user_id=request.user_id,
            session_id=request.session_id,
            user_response=request.user_response
        )
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Session error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mock-interview/evaluate")
async def evaluate_interview(request: MockEvaluateRequest):
    """Ends the session and runs the Interview Evaluator Agent."""
    try:
        result = await runner.evaluate_interview(
            user_id=request.user_id,
            session_id=request.session_id
        )
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Evaluation failed"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/resume-analyze")
async def analyze_resume(request: ResumeAnalysisRequest):
    """Analyze Resume vs Job Description"""
    try:
        result = await runner.run_resume_analysis(
            user_id=request.user_id,
            resume_text=request.resume_text,
            jd=request.job_description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate")
async def evaluate_response(request: EvalRequest):
    """Run LLM-as-a-Judge"""
    return await runner.run_quality_check(request.user_prompt, request.ai_response)

@router.get("/traces")
async def get_traces():
    """Get observability logs"""
    traces = []
    try:
        with open("/app/data/agent_traces.jsonl", "r") as f:
            for line in f:
                traces.append(json.loads(line))
        return {"traces": traces[-10:]} # Return last 10 runs
    except FileNotFoundError:
        return {"traces": []}

# =========================================================================
# ℹ️ SYSTEM INFO
# =========================================================================
@router.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {
                "name": "StudyAgent",
                "description": "Creates personalized study plans",
                "tools": ["google_search", "productivity_analyzer"]
            },
            {
                "name": "JobSearchAgent",
                "description": "Helps with career planning and job search",
                "tools": ["google_search"]
            },
            {
                "name": "WellnessAgent",
                "description": "Provides wellness and stress management tips",
                "tools": ["wellness_tips"]
            },
            {
                "name": "InterviewAgent",
                "description": "Prepares for company-specific interviews",
                "tools": ["interview_research", "google_search"]
            },
            {
                "name": "QuizAgent",
                "description": "Generates learning quizzes from topics",
                "tools": ["quiz_generator"]
            },
            {
                "name": "PlannerAgent",
                "description": "Combines all plans into cohesive schedule",
                "tools": []
            }
        ]
    }