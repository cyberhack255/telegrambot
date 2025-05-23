import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load environment variables
load_dotenv()

# Required credentials
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Telegram chat IDs
source_channel = -1001524646321  # Replace with actual source channel ID
destination_chat = -1002315854792  # Replace with actual destination chat ID

# Session name for user login
session_name = 'copy_paste_user'

# Initialize Telegram client
client = TelegramClient(session_name, api_id, api_hash)

async def start_client():
    await client.start()
    me = await client.get_me()
    print(f"🚀 Logged in as: {me.username or me.first_name} (ID: {me.id})")
    print(f"📨 Listening for messages in chat ID: {source_channel}")

    @client.on(events.NewMessage(chats=source_channel))
    async def forward_message(event):
        try:
            await event.forward_to(destination_chat)
            print(f"✅ Forwarded message: {event.message.text or '[Non-text content]'}")
        except Exception as e:
            print(f"❌ Error forwarding message: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(start_client())
