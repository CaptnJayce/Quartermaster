import asyncio
import os
from enum import Enum, auto
from web_search import search_web
from audio import generate_speech, play_audio
from media_controller import forward, rewind, playpause
import ollama

# Use Enum for modes
class Mode(Enum):
    QUERY = auto()
    MEDIA = auto()
    SILENT = auto()

class Assistant:
    def __init__(self):
        self.conversation_history = []
        self.mode = Mode.QUERY

    async def query_llama(self, query):
        try:
            import prompt 
            prompt_text = prompt.p
            for message in self.conversation_history:
                prompt_text += f"\n{message['role']}: {message['content']}"
            prompt_text += f"\nUser: {query}\nAssistant:"

            result = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt_text}])
            return result['message']['content'] if 'message' in result and 'content' in result['message'] else "No content in response"
        except Exception as e:
            print(f"Error querying Ollama: {e}")
            return None

    async def handle_audio_response(self, text):
        try:
            await generate_speech(text)
            play_audio("response.mp3")
        finally:
            if os.path.exists("response.mp3"):
                os.remove("response.mp3")

    async def handle_query_mode(self, query):
        reply = await self.query_llama(query)
        if not reply:
            return

        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": reply})

        if "search" not in query.lower():
            print(f"\nAssistant: {reply}")
            await self.handle_audio_response(reply)
        else:
            search_results = search_web(query)
            if search_results:
                relevant_info = "\n".join(
                    f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n"
                    for result in search_results[:3]
                )
                formatted_query = f"Please summarise the following into a concise summary:\n\n{relevant_info}"
                summary = await self.query_llama(formatted_query)
                if summary:
                    print(summary + "\n")
                    await self.handle_audio_response(summary)

    async def handle_media_mode(self, query):
        if "play" in query.lower() or "resume" in query.lower():
            playpause()
        elif "pause" in query.lower() or "stop" in query.lower():
            playpause()
        elif "rewind" in query.lower() or "previous" in query.lower():
            rewind()
        elif "next" in query.lower() or "forward" in query.lower():
            forward()

    async def assistant(self, query):
        query = query.lower()
        if "query mode" in query:
            self.mode = Mode.QUERY
            print("Query mode activated.")
        elif "media mode" in query:
            self.mode = Mode.MEDIA
            print("Media mode activated.")
        elif "silent mode" in query:
            self.mode = Mode.SILENT
            print("Silent mode activated.")
        elif query == "assistant exit":
            exit()

        if self.mode == Mode.QUERY:
            await self.handle_query_mode(query)
        elif self.mode == Mode.MEDIA:
            await self.handle_media_mode(query)
        elif self.mode == Mode.SILENT:
            pass 
