from web_search import search_web
from audio import generate_speech, play_audio
import spotify
import asyncio
import os
import ollama

conversation_history = []

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
    wake_words = ["qt", "quartermaster", "cutie"] # will add option to customise later
    shutdown_words = ["shutdown", "shut down", "exit", "quit"]
    spotify_words = ["skip", "next", "pause", "stop", "rewind", "play", "resume", "playlist", "like", "favourite"]
    
    reply = query_llama(query)

    if any(word in query.lower() for word in wake_words) and any(word in query.lower() for word in shutdown_words):
        print("shutdown")
        exit()
    
    if any(word in query.lower() for word in spotify_words):
        if "skip" in query.lower() or "next" in query.lower():
            spotify.skip_song()
        if "pause" in query.lower() or "stop" in query.lower():
            spotify.pause_song()
        if "rewind" in query.lower():
            spotify.rewind_song()
        if "play" in query.lower() or "resume" in query.lower():
            spotify.resume_song()
        if "like" in query.lower() or "favourite" in query.lower():
            spotify.like_song()

    elif reply:
        conversation_history.append({"role": "user", "content": query})
        conversation_history.append({"role": "assistant", "content": reply})

        if "search" not in query.lower():
            print("\nAssistant:", reply)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(generate_speech(reply))
                play_audio("response.mp3")
            finally:
                loop.close()

            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

        if "search" in query.lower() or "search the web" in reply.lower():
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
                        play_audio("response.mp3")
                    finally:
                        loop.close()
                    if os.path.exists("response.mp3"):
                        os.remove("response.mp3")