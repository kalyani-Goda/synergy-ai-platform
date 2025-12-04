import random
from datetime import datetime

def get_personalized_wellness_tip(stress_level: int = 0) -> dict:
    """Wellness tip based on stress level and time of day"""
    tips_by_stress = {
        0: ["Take a 5-minute meditation break", "Practice gratitude journaling", "Do 10 minutes of light stretching"],
        1: ["Try 4-7-8 breathing technique", "Take a 10-minute walk", "Listen to calming music"],
        2: ["Use Pomodoro technique", "Practice progressive muscle relaxation", "Write down your thoughts"],
        3: ["Take a 30-minute digital detox", "Call a friend", "Practice deep breathing"]
    }
    
    current_hour = datetime.now().hour
    time_advice = "Morning tip" if current_hour < 12 else "Afternoon tip" if current_hour < 17 else "Evening tip"
    
    tips = tips_by_stress.get(stress_level, tips_by_stress[1])
    selected_tip = random.choice(tips)
    
    return {
        "status": "success",
        "tip": f"{selected_tip}. {time_advice}",
        "stress_level": stress_level,
        "timestamp": datetime.now().isoformat()
    }