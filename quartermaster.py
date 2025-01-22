import requests
from bs4 import BeautifulSoup
import ollama
import edge_tts
import pygame
import asyncio
import speech_recognition as sr
import os
import qt  # Create a file called qt.py and add your prompt there (p = f""" """)
import time

# Init recognizer
r = sr.Recognizer()

conversation_history = []

# Currently using en-IE-EmilyNeural
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

def listen_for_audio(prompt="Listening..."):
    with sr.Microphone() as source:
        print(prompt)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You said: " + said)
        except Exception as e:
            pass
            #print("Exception " + str(e))
    return said

def query_llama(query):
    try:
        prompt = qt.p

        for message in conversation_history:
            prompt += f"\n{message['role']}: {message['content']}"

        prompt += f"\nUser: {query}\nQT:"
        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])

        return result['message']['content'] if 'message' in result and 'content' in result['message'] else "No content in response"

    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def search_web(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0 '
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = []

    for g in soup.find_all(class_='tF2Cxc'):
        title = g.find('h3').text
        link = g.find('a')['href']
        snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else 'No snippet available'
        search_results.append({"title": title, "link": link, "snippet": snippet})

    return search_results

def qt_assistant(query):
    qt_reply = query_llama(query)

    if qt_reply:
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": qt_reply})

        if "search" not in query.lower():
            print("\nQT:", qt_reply)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(generate_speech(qt_reply))
                play_audio(OUTPUT_FILE)
            finally:
                loop.close()

            if os.path.exists(OUTPUT_FILE):
                os.remove(OUTPUT_FILE)

        if "search" in query.lower() or "search the web" in qt_reply.lower():
            search_results = search_web(query)

            if search_results:
                relevant_info = ""
                for idx, result in enumerate(search_results[:3], 1):
                    relevant_info += f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n\n"

                formatted_query = f"Please summarize the following search results into a concise, human-readable summary:\n\n{relevant_info}"
                summary = query_llama(formatted_query)

                if summary:
                    print(summary + "\n")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(generate_speech(summary))
                        play_audio(OUTPUT_FILE)
                    finally:
                        loop.close()

                    if os.path.exists(OUTPUT_FILE):
                        os.remove(OUTPUT_FILE)
                else:
                    print("No summary returned from Ollama.")

def command_words():
    wake_words = ["qt", "quartermaster", "cutie"]
    shutdown_words = ["shutdown", "shut down", "exit", "quit"]
    
    while True:
        said = listen_for_audio(prompt="Say 'Quartermaster'")
        for word in wake_words:
            if any(word in said.lower() for word in wake_words) and any(word in said.lower() for word in shutdown_words):
                print("shutdown")
                exit()
            
            elif any(word in said.lower() for word in wake_words):
                print("waking")     
                return True
      
def listen_with_timer(timeout):
    print(f"{timeout} seconds to speak...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        query = listen_for_audio(prompt="Listening...")
        if query.strip():
            return query
    return None

if __name__ == "__main__":
    while True:
        command_words()
        while True:
            query = listen_with_timer(timeout=5)
            if query:
                qt_assistant(query)
            else:
                break
