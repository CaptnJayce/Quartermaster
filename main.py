from audio import listen_with_timer
from assistant import assistant
from settings import assistant_name, custom_prompt, music_control

if __name__ == "__main__":
    assistant_name()
    custom_prompt()
    music_control()
      
    while True:
        query = listen_with_timer(timeout=5)
        if query:
            assistant(query)
        else:
            break
