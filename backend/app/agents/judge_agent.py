
from google.adk.agents import LlmAgent
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt # Import the loader

judge_agent = LlmAgent(
    model=gemini_model,
    name="QualityJudgeAgent",
    instruction=load_prompt("judge.yaml"), # Load from file
    output_key="evaluation_report"
)