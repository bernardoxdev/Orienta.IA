from pyrogram import Client, filters
from pyrogram.types import Message

from passlib.context import CryptContext

from backend.utils.telegram_state_utils import set_state
from backend.utils.user_utils import exists_user_telegram
from backend.utils.register_utils import register_infos

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def register(app: Client):
    @app.on_message(filters.command("logar"))
    async def logar_command(client: Client, message: Message):
        telegram_id = str(message.from_user.id)

        if await exists_user_telegram(telegram_id):
            await message.reply_text("Você ja se registrou ou fez login.")
            return

        register_infos[telegram_id] = {}

        set_state(telegram_id, "esperando_email_logar")

        await message.reply_text("Envie seu email para logar: ")

if __name__ == '__main__':
    pass