from audio import listen_with_timer
from assistant import assistant 
from settings import user_name, assistant_name, custom_prompt, save_settings, load_settings

if __name__ == "__main__":
    settings = load_settings()
    if settings.get('first_launch', True):
        user_name(settings)
        assistant_name(settings)
        custom_prompt(settings)

        settings['first_launch'] = False
        save_settings(settings)
   

    while True:
        query = listen_with_timer(timeout=5)
        if query:
            assistant(query)
        else:
            pass
