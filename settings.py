import json
import os

def save_settings(settings, filename="settings.json"):
    with open(filename, 'w') as file:
        json.dump(settings, file, indent=4)

def load_settings(filename="settings.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def assistant_name():
    settings = load_settings()
    print("What would you like your assistant to be called? (Leave blank for Quartermaster)")
    name = input("Enter: ")
    settings['assistant_name'] = name if name else "Quartermaster"
    save_settings(settings)

def custom_prompt():
    settings = load_settings()
    print("Would you like to add a custom prompt? (Leave blank for no)")
    prompt_check = input("Enter: ")
    
    if prompt_check.lower() != "yes":
        settings['custom_prompt'] = False
    else:
        settings['custom_prompt'] = True
    save_settings(settings)

def music_control():
    settings = load_settings()
    print("Will you use Spotify for music? (Leave blank for no)")
    music_check = input("Enter: ")
    
    if music_check.lower() != "yes":
        settings['use_spotify'] = False
    else:
        settings['use_spotify'] = True
    save_settings(settings)