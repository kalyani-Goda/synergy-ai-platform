

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .base import gemini_model, interview_tool
from ..prompts.prompt_loader import load_prompt  # <--- Import the loader

# 1. Interview Search Agent
# Finds raw information about the company and role using Google Search
interview_search_agent = LlmAgent(
    model=gemini_model,
    name="InterviewSearchAgent",
    instruction=load_prompt("interview_search.yaml"), # <--- Load from YAML
    tools=[google_search], 
    output_key="raw_interview_research" 
)

# 2. Interview Processor Agent
# Uses your custom 'interview_tool' to structure the data
interview_agent = LlmAgent(
    model=gemini_model,
    name="InterviewProcessorAgent", 
    instruction=load_prompt("interview_processor.yaml"), # <--- Load from YAML
    tools=[interview_tool], 
    output_key="interview_plan"
)

# 3. Interview Planner Agent
# Formats everything into a beautiful markdown guide
interview_planner_agent = LlmAgent(
    model=gemini_model,
    name="InterviewPlannerAgent",
    instruction=load_prompt("interview_planner.yaml"), # <--- Load from YAML
    output_key="final_interview_prep"
)