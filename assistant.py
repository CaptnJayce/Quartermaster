from web_search import search_web
from audio import generate_speech, listen_for_audio, play_audio
import asyncio
import os
import ollama

conversation_history = []

def query_llama(query):
    import qt  # prompt should be in qt.py

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
                play_audio("response.mp3")
            finally:
                loop.close()

            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

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
                        play_audio("response.mp3")
                    finally:
                        loop.close()
                    if os.path.exists("response.mp3"):
                        os.remove("response.mp3")

def command_words():
    wake_words = ["qt", "quartermaster", "cutie"]
    shutdown_words = ["shutdown", "shut down", "exit", "quit"]

    while True:
        said = listen_for_audio(prompt="Say 'Quartermaster'")
        if any(word in said.lower() for word in wake_words) and any(word in said.lower() for word in shutdown_words):
            print("shutdown")
            exit()
        elif any(word in said.lower() for word in wake_words):
            print("waking")
            return True
