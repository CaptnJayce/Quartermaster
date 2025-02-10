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

def user_name(settings):
    print("What is your username?")
    name = input("Enter: ")
    settings['username'] = name

def assistant_name(settings):
    print("What would you like your assistant to be called? (Leave blank for Quartermaster)")
    name = input("Enter: ")
    settings['assistant_name'] = name if name.strip() else "Quartermaster"

def custom_prompt(settings):
    print("Would you like to add a custom prompt? (Leave blank for no)")
    settings['custom_prompt'] = input("Enter: ").lower() == "yes"

def music_control(settings):
    print("Will you use Spotify for music? (Leave blank for no)")
    settings['use_spotify'] = input("Enter: ").lower() == "yes"