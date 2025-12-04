from google.adk.agents import ParallelAgent, SequentialAgent, LlmAgent
from .study_agent import study_research_agent, study_planner_agent
from .job_search_agent import job_search_agent, web_search_agent_simple, job_coordinator_agent_simple
from .wellness_agent import wellness_agent
from .interview_agent import interview_search_agent, interview_agent, interview_planner_agent
from .quiz_agent import quiz_agent
from .base import gemini_model
from ..prompts.prompt_loader import load_prompt  # <--- Import Loader

# 1. Planner Agent (The Finalizer)
planner_agent = LlmAgent(
    model=gemini_model,
    name="PlannerAgent",
    instruction=load_prompt("daily_planner.yaml"), # <--- Load from YAML
    output_key="daily_plan"
)

# --- Compositions ---

# Study Workflow
study_workflow = SequentialAgent(
    name="StudyWorkflow",
    sub_agents=[study_research_agent, study_planner_agent],
)

# Daily Parallel Execution
daily_parallel_agents = ParallelAgent(
    name="DailySpecialists",
    sub_agents=[
        study_workflow, 
        job_search_agent, 
        wellness_agent
    ],
)

# Final Daily Workflow
daily_workflow = SequentialAgent(
    name="DailyPlannerWorkflow",
    sub_agents=[daily_parallel_agents, planner_agent],
)

# Interview Workflow
interview_workflow = SequentialAgent(
    name="InterviewWorkflow",
    sub_agents=[
        interview_search_agent,      # Step 1: Gets raw research using Google Search
        interview_agent,             # Step 2: Processes research and uses custom tool
        interview_planner_agent,     # Step 3: Formats the final output
    ], 
)

# Quiz Workflow
quiz_workflow = SequentialAgent(
    name="QuizWorkflow",
    sub_agents=[quiz_agent],
)

# Job Search Workflow
simple_job_search = SequentialAgent(
    name="SimpleJobSearch",
    sub_agents=[web_search_agent_simple, job_coordinator_agent_simple],
)