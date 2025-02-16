import asyncio
from audio import listen_with_timer
from assistant import Assistant 
from settings import user_name, assistant_name, custom_prompt, save_settings, load_settings

async def main():
    settings = load_settings()
    if settings.get('first_launch', True):
        user_name(settings)
        assistant_name(settings)
        custom_prompt(settings)

        settings['first_launch'] = False
        save_settings(settings)
   
    assistant_instance = Assistant()

    while True:
        query = listen_with_timer(timeout=5)
        if query:
            await assistant_instance.assistant(query)
        else:
            pass

if __name__ == "__main__":
    asyncio.run(main())
