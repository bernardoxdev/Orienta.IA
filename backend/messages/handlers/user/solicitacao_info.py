from pyrogram import Client, filters
from pyrogram.types import Message

from backend.utils.user_utils import exists_user_telegram
from backend.utils.register_utils import verificar_vinculado
from backend.utils.solicitacoes_utils import get_solicitacao_by_telegram
from backend.utils.universidade_utils import get_universidade_nome_by_id

def register(app: Client):
    @app.on_message(filters.command("solicitacao_info"))
    async def solicitacao_info(client: Client, message: Message):
        telegram_id = str(message.from_user.id)

        if not await exists_user_telegram(telegram_id):
            await message.reply_text(
                "Você ainda não se registrou ou não vinculou sua conta ao Telegram.\n\n"
                "Caso não tenha se registrado utilize /registrar.\n"
                "Caso já tenha uma conta, acesse o site e vincule seu Telegram."
            )
            return

        if await verificar_vinculado(telegram_id):
            await message.reply_text("Sua conta já está vinculada.")
            return

        solicitacao = await get_solicitacao_by_telegram(telegram_id)

        if solicitacao is None:
            await message.reply_text("Você não possui uma solicitação de vínculo pendente.")
            return

        nome_universidade = await get_universidade_nome_by_id(solicitacao.universidade_id)

        texto = (
            "📄 **Solicitação de Vínculo**\n\n"
            f"Tipo: {solicitacao.tipo}\n"
            f"Universidade ID: {nome_universidade}\n"
        )

        if solicitacao.matricula:
            texto += f"Matrícula: {solicitacao.matricula}\n"

        if solicitacao.departamento:
            texto += f"Departamento: {solicitacao.departamento}\n"

        await message.reply_text(texto)

if __name__ == "__main__":
    pass