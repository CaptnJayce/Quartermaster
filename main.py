from audio import listen_with_timer
from assistant import assistant

if __name__ == "__main__":
    while True:
        query = listen_with_timer(timeout=5)
        if query:
            assistant(query)
        else:
            break
