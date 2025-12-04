import os
import yaml

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_prompt(filename: str) -> str:
    """Loads a prompt instruction from a YAML file."""
    file_path = os.path.join(BASE_DIR, filename)
    
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get('instruction', '')
    except FileNotFoundError:
        print(f"⚠️ Warning: Prompt file {filename} not found.")
        return ""
    except Exception as e:
        print(f"❌ Error loading prompt {filename}: {e}")
        return ""