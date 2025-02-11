import pygame
import edge_tts
import time

# currently using EmilyNeural
VOICES = ['en-AU-NatashaNeural', 'en-CA-ClaraNeural', 'en-GB-LibbyNeural', 'en-IN-NeerjaNeural', 'en-IE-EmilyNeural']
VOICE = VOICES[4]
SPEED = "+75%"
OUTPUT_FILE = "response.mp3"

async def generate_speech(text: str) -> None:
    communicate = edge_tts.Communicate(text, VOICE, rate=SPEED)
    await communicate.save(OUTPUT_FILE)

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

def listen_for_audio():
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You said: " + said)
        except Exception:
            pass
    return said

def listen_with_timer(timeout):
    start_time = time.time()
    while time.time() - start_time < timeout:
        query = listen_for_audio()
        if query.strip():
            return query
    return None
