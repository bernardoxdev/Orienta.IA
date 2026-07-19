from pyrogram import Client, filters
from pyrogram.types import Message

from backend.utils.user_utils import exists_user_telegram
from backend.utils.register_utils import register_infos, verificar_vinculado
from backend.utils.solicitacoes_utils import has_solicitacao_by_telegram
from backend.utils.telegram_state_utils import set_state

def register(app: Client):
    @app.on_message(filters.command("vincular"))
    async def vincular(client: Client, message: Message):
        telegram_id = str(message.from_user.id)

        if not await exists_user_telegram(telegram_id):
            await message.reply_text(
                "Voce ainda nao se registrou ou nao vinculou sua conta ao telegram.\n"
                "Caso nao tenha se registrado utilize /registrar\n"
                "Caso ja tenha uma conta acesse o site e vincule seu telegram a ela"
            )
            return

        if await verificar_vinculado(telegram_id):
            await message.reply_text("Sua conta ja foi vinculada.")
            return

        if await has_solicitacao_by_telegram(telegram_id):
            await message.reply_text("Você já possui uma solicitação de vínculo pendente.")
            return

        if len(message.command) < 2:
            await message.reply_text(
                "Uso correto:\n"
                "/vincular professor\n"
                "/vincular aluno"
            )
            return

        register_infos[telegram_id] = {}

        tipo = message.command[1].lower()
        register_infos[telegram_id]["tipo"] = tipo

        if tipo == "professor":
            set_state(telegram_id, "esperando_vinculo_professor")

            await message.reply_text("Envie a SIGLA ou NOME da universidade:")
            return

        elif tipo == "aluno":
            set_state(telegram_id, "esperando_vinculo_aluno")

            await message.reply_text("Envie a SIGLA ou NOME da universidade:")
            return

        await message.reply_text("Tipo inválido.\nUse /vincular professor ou /vincular aluno")

if __name__ == '__main__':
    pass