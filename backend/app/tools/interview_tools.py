from datetime import datetime

def search_interview_questions_meta(company: str, role: str) -> dict:
    """Helper to structure interview search data"""
    search_query = f"{company} {role} interview questions site:glassdoor.com OR site:leetcode.com"
    return {
        "company": company,
        "role": role,
        "search_query": search_query,
        "common_topics": ["Data Structures", "System Design", "Behavioral Questions"],
        "searched_at": datetime.now().isoformat()
    }