import uuid
from datetime import datetime

def generate_quiz_structure(topic: str, notes: str = "", difficulty: str = "medium") -> dict:
    """Generate quiz metadata structure (LLM fills content)"""
    quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"
    return {
        "quiz_id": quiz_id,
        "topic": topic,
        "difficulty": difficulty,
        "generated_at": datetime.now().isoformat()
    }