from pyrogram import Client, filters
from passlib.context import CryptContext

from backend.utils.telegram_state_utils import (
    set_state,
    get_state,
    clear_state
)
from backend.utils.user_utils import (
    get_user_by_telegram_id,
    criar_usuario
)

register_infos = {}

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def register(app: Client):
    @app.on_message(filters.command("registrar"))
    async def start_register(client, message):
        telegram_id = str(message.from_user.id)

        if get_user_by_telegram_id(telegram_id):
            await message.reply(
                "Você já está registrado!"
            )
            return

        register_infos[telegram_id] = {}

        set_state(telegram_id, "esperando_nome")

        await message.reply(
            "Envie seu nome completo:"
        )

    @app.on_message(filters.text & ~filters.command(["registrar"]))
    async def register_form(client, message):
        telegram_id = str(message.from_user.id)
        state = get_state(telegram_id)

        if not state:
            return

        if state == "esperando_nome":
            register_infos[telegram_id]["nome"] = message.text

            set_state(telegram_id, "esperando_email")

            await message.reply(
                "Agora envie seu email:"
            )

            return

        if state == "esperando_email":
            register_infos[telegram_id]["email"] = message.text

            set_state(telegram_id, "esperando_senha")

            await message.reply(
                "Agora envie sua senha:"
            )

            return

        if state == "esperando_senha":
            register_infos[telegram_id]["senha"] = message.text

            data = register_infos[telegram_id]

            await criar_usuario(
                telegram_id=telegram_id,
                nome=data["nome"],
                email=data["email"],
                senha=pwd_context.hash(data["senha"])
            )

            clear_state(telegram_id)

            register_infos.pop(telegram_id, None)

            await message.reply(
                "Registro realizado com sucesso!"
            )

if __name__ == '__main__':
    pass