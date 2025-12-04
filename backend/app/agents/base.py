# backend/app/agents/base.py
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from ..core.config import settings
from ..llm.retry_config import retry_config
from ..tools import wellness_tools, productivity_tools, quiz_tools, interview_tools

# 1. Initialize Model
gemini_model = Gemini(
    model="gemini-2.5-flash", 
    retry_options=retry_config, 
    api_key=settings.GOOGLE_API_KEY
)

# 2. Initialize Function Tools
wellness_tool = FunctionTool(wellness_tools.get_personalized_wellness_tip)
productivity_tool = FunctionTool(productivity_tools.analyze_productivity_patterns)
quiz_tool = FunctionTool(quiz_tools.generate_quiz_structure)
interview_tool = FunctionTool(interview_tools.search_interview_questions_meta)