from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt  # <--- Import loader

# 1. Standard Job Advisor (For Daily Planner)
job_search_agent = LlmAgent(
    model=gemini_model,
    name="JobSearchAgent",
    instruction=load_prompt("job_advisor.yaml"), # <--- Load from YAML
    tools=[google_search],
    output_key="job_plan"
)

# --- WORKFLOW AGENTS (For Job Search Tab) ---

# 2. Web Searcher (Finds the raw data)
web_search_agent_simple = LlmAgent(
    model=gemini_model,
    name="WebSearchAgentSimple",
    instruction=load_prompt("job_web_searcher.yaml"), # <--- Load from YAML
    tools=[google_search],
    output_key="search_results"
)

# 3. Coordinator (Formats the report)
job_coordinator_agent_simple = LlmAgent(
    model=gemini_model,
    name="JobSearchCoordinatorSimple",
    instruction=load_prompt("job_coordinator.yaml"), # <--- Load from YAML
    output_key="job_search_report"
)