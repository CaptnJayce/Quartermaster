from audio import listen_with_timer
from assistant import assistant
from settings import assistant_name, custom_prompt, load_settings, music_control, save_settings
import json

if __name__ == "__main__":
    settings = load_settings()
    if settings['first_launch'] == False:
        assistant_name()
        custom_prompt()
        music_control()
        settings['first_launch'] = True
        save_settings(settings)

    while True:
        query = listen_with_timer(timeout=5)
        if query:
            assistant(query)
        else:
            break
