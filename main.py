from audio import listen_with_timer
from assistant import qt_assistant, command_words

if __name__ == "__main__":
    while True:
        command_words()
        while True:
            query = listen_with_timer(timeout=5)
            if query:
                qt_assistant(query)
            else:
                break
