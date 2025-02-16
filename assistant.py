from web_search import search_web
from audio import generate_speech, play_audio
from media_controller import forward, rewind, playpause
from enum import Enum, auto
import asyncio
import os
import ollama

conversation_history = []

class Mode(Enum):
    QUERY = auto()
    MEDIA = auto()
    SILENT = auto()


mode = Mode.QUERY

def query_llama(query):
    import prompt  # prompt should be in prompt.py

    try:
        prompt = prompt.p
        for message in conversation_history:
            prompt += f"\n{message['role']}: {message['content']}"

        prompt += f"\nUser: {query}\nAssistant:"
        result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
        return result['message']['content'] if 'message' in result and 'content' in result['message'] else "No content in response"
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def assistant(query):
    global mode 

    if "query mode" in query.lower():
        mode = Mode.QUERY
        print("query mode")
    if "media mode" in query.lower():
        mode = Mode.MEDIA
        print("media mode")
    if "silent mode" in query.lower():
        mode = Mode.SILENT
        print("silent mode")
            
    if query.lower() == "assistant exit":
        exit()

    if mode == Mode.QUERY: ## Query mode
        reply = query_llama(query)

        conversation_history.append({"role": "user", "content": reply})
        conversation_history.append({"role": "assistant", "content": reply})

        if "search" not in query.lower():
            print("\nAssistant:", reply)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(generate_speech(str(reply)))
                play_audio("response.mp3")
            finally:
                loop.close()

            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

        if "search" in query.lower():
            search_results = search_web(query)
            if search_results:
                relevant_info = ""
                for idx, result in enumerate(search_results[:3], 1):
                    relevant_info += f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n\n"

                formatted_query = f" Please provide a concise summary of the following information as short as possible. Focus on the key points and avoid unnecessary details:\n\n{relevant_info}"
                summary = query_llama(formatted_query)
                if summary:
                    print(summary + "\n")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(generate_speech(summary))
                        play_audio("response.mp3")
                    finally:
                        loop.close()
                    if os.path.exists("response.mp3"):
                        os.remove("response.mp3")

    if mode == Mode.MEDIA: ## Media mode
        if "play" in query.lower() or "resume" in query.lower():
            playpause()

        if "pause" in query.lower() or "stop" in query.lower():
            playpause()

        if "rewind" in query.lower() or "previous" in query.lower():
            rewind()

        if "next" in query.lower() or "forward" in query.lower():
            forward()

    if mode == Mode.SILENT: ## Silent mode
        pass
