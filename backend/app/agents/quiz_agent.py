from google.adk.agents import LlmAgent
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt # Import the loader

# Quiz Generator Agent
# In your main.py, this agent didn't use the tool directly but generated content based on prompt instructions
quiz_agent = LlmAgent(
    model=gemini_model,
    name="QuizAgent",
    instruction=load_prompt("quiz.yaml"),
    tools=[], 
    output_key="quiz_content"
)