from google.adk.agents import LlmAgent
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt # Import the loader

# 1. Interactive Interviewer
# This agent runs in a loop, asking one question at a time
interactive_interviewer = LlmAgent(
    model=gemini_model,
    name="MockInterviewerAgent",
    instruction=load_prompt("interactive_interviewer.yaml"),
    tools=[], 
    output_key="interview_transcript_segment"
)

# 2. Interview Evaluator
# This agent runs once at the end to grade the session
interview_evaluator = LlmAgent(
    model=gemini_model,
    name="EvaluatorAgent",
    instruction=load_prompt("interview_evaluator.yaml"),
    tools=[], 
    output_key="final_interview_summary"
)