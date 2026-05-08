from pyrogram import Client

from backend.core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_ID
from backend.messages.handlers import start, register

app = Client(
    name="bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_ID,
    in_memory=True
)

start.register(app)
register.register(app)

if __name__ == '__main__':
    app.run()