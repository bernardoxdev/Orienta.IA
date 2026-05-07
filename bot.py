from pyrogram import Client

from backend.config.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_ID
from backend.messages.handlers import start

app = Client(
    name="bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_ID,
    in_memory=True
)

start.register(app)

if __name__ == '__main__':
    app.run()