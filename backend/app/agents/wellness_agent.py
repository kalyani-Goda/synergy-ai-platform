from google.adk.agents import LlmAgent
from .base import gemini_model, wellness_tool
from ..prompts.prompt_loader import load_prompt
# Wellness Agent
wellness_agent = LlmAgent(
    model=gemini_model,
    name="WellnessAgent",
    instruction=load_prompt("wellness.yaml"),
    tools=[wellness_tool],
    output_key="wellness_plan"
)