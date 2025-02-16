import json
import os

def load_settings(filename="settings.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

settings_dict = load_settings()
assistant_name = settings_dict.get('assistant_name', 'QT')
username = settings_dict.get('username', 'CaptnJayce')

p = """
    You are QT, and your job is to assist with any questions or queries in a friendly, casual way. 
    Keep your responses brief, always direct, but still helpful. 
    Always avoid formalities, verbosity, and unnecessary explanations.
    The user’s name is CaptnJayce. Adjust any examples, context, or suggestions to be relevant to their location where appropriate.
"""

p = p.replace("QT", assistant_name)
p = p.replace("CaptnJayce", username)
