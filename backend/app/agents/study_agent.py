from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .base import gemini_model, productivity_tool
from ..prompts.prompt_loader import load_prompt

# 1. Study Research Agent
# Uses Google Search to find relevant study resources
study_research_agent = LlmAgent(
    model=gemini_model,
    name="StudyResearchAgent",
    instruction=load_prompt("study_research.yaml"),
    tools=[google_search], 
    output_key="study_research_output"
)

# 2. Study Planner Agent
# Uses productivity_tool to create a focused study plan
study_planner_agent = LlmAgent(
    model=gemini_model,
    name="StudyPlannerAgent",
    instruction=load_prompt("study_planner.yaml"),
    tools=[productivity_tool],
    output_key="study_plan"
)