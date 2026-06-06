from pyrogram import Client, filters
from pyrogram.types import Message

from backend.utils.user_utils import get_role_user_telegram_id

ROLE_MESSAGES = {
    "admin": (""
              ""),
    "professor": (""
                  ""),
    "aluno": (""
                  ""),
    "user": ("/vincular <professor/aluno> - Vincule sua conta a sua universidade para desbloquear funcionalidades específicas para seu perfil\n"
              "/projetos - Veja os projetos que estao em andamentos\n"
              "/universidades - Veja a lista de todas as universidades cadastradas\n"
              "/professores - Veja a lista de todos os professores cadastrados\n"),
    "pessoa": ("👋 Olá! Eu sou o bot Orienta.IA.\n"
             "Criando por Bernardo de Castro.\n\n"
             "Comandos disponíveis:\n"
             "/start - Iniciar\n"
             "/help - Ajuda\n"
             "/registrar - Registrar telegram na plataforma\n"
             "/logar - Realizar login na plataforma\n")
}

def register(app: Client):
    @app.on_message(filters.command("start") | filters.command("help"))
    async def start(client: Client, message: Message):
        telegram_id = str(message.from_user.id)

        msg = ROLE_MESSAGES.get("pessoa") + ROLE_MESSAGES.get(await get_role_user_telegram_id(telegram_id), "Se registre para desbloquear todas as funcionalidades do bot.")

        await message.reply_text(msg)

if __name__ == '__main__':
    pass