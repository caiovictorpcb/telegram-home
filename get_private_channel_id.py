import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
API_ID = os.environ.get("TELEGRAM_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH")
channel_link = ''

client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    await client.start()


    entity = await client.get_input_entity(channel_link)
    print(entity)

    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
