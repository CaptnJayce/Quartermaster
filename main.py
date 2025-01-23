from audio import listen_with_timer, play_audio, generate_speech
from assistant import qt_assistant, command_words
import os

if __name__ == "__main__":
    while True:
        command_words()
        while True:
            query = listen_with_timer(timeout=5)
            if query:
                qt_assistant(query)
            else:
                break
