from google.adk.agents import LlmAgent
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt # Import the loader

# Resume ATS Agent
resume_agent = LlmAgent(
    model=gemini_model,
    name="ResumeATS_Agent",
    instruction=load_prompt("resume.yaml"),
    output_key="resume_analysis_report"
)