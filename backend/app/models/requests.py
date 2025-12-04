from pydantic import BaseModel
from typing import List, Optional

class DailyPlanRequest(BaseModel):
    user_id: str
    goals: str
    session_id: Optional[str] = None
    stress_level: Optional[int] = 1

class InterviewRequest(BaseModel):
    user_id: str
    role: str
    company: str
    description: Optional[str] = None

class QuizRequest(BaseModel):
    user_id: str
    topic: str
    notes: Optional[str] = ""
    difficulty: str = "medium"

class MockStartRequest(BaseModel):
    user_id: str
    role: str
    company: str
    common_topics: List[str]

class MockContinueRequest(BaseModel):
    user_id: str
    session_id: str
    user_response: str

class MockEvaluateRequest(BaseModel):
    user_id: str
    session_id: str

class JobSearchRequest(BaseModel):
    user_id: str
    role: str
    level: str
    experience: int
    location: str

class ResumeAnalysisRequest(BaseModel):
    user_id: str
    resume_text: str
    job_description: str

class EvalRequest(BaseModel):
    user_prompt: str
    ai_response: str
