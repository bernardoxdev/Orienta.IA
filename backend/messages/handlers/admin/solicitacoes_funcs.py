import math

from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from backend.utils.user_utils import exists_user_telegram
from backend.utils.administrador_utils import is_user_admin_by_telegram
from backend.utils.solicitacoes_utils import get_solicitacoes

from backend.database.models.solicitacoes_vincular import SolicitacaoVincular

PAGE_SIZE = 3

def create_page(solicitacoes: List[SolicitacaoVincular], page: int):
    total_pages = math.ceil(len(solicitacoes) / PAGE_SIZE)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    current = solicitacoes[start:end]

    text = "📚 Lista de Solicitaçoes\n\n"

    for solicitacao in current:
        text = (
            "📄 **Solicitação de Vínculo**\n\n"
            f"Tipo: {solicitacao.tipo}\n"
            f"Universidade ID: {solicitacao.universidade_id}\n"
        )

        if solicitacao.matricula:
            text += f"Matrícula: {solicitacao.matricula}\n"

        if solicitacao.departamento:
            text += f"Departamento: {solicitacao.departamento}\n"

    text += f"\nPágina {page + 1}/{total_pages}"

    buttons = []
    navigation = []

    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️", callback_data=f"solicitacoes:{page - 1}"))

    if page < total_pages - 1:
        navigation.append(InlineKeyboardButton("➡️", callback_data=f"solicitacoes:{page + 1}"))

    if navigation:
        buttons.append(navigation)

    keyboard = InlineKeyboardMarkup(buttons) if buttons else None

    return text, keyboard

def register(app: Client):
    @app.on_message(filters.command("solicitacoes"))
    async def vincular(client: Client, message: Message):
        telegram_id = str(message.from_user.id)

        if not await exists_user_telegram(telegram_id):
            await message.reply_text(
                "Você ainda não se registrou ou não vinculou sua conta ao Telegram.\n\n"
                "Caso não tenha se registrado utilize /registrar.\n"
                "Caso já tenha uma conta, acesse o site e vincule seu Telegram."
            )
            return

        if not await is_user_admin_by_telegram(telegram_id):
            await message.reply_text(
                "Você não tem permissão para acessar esta funcionalidade."
            )
            return

        solicitacoes = await get_solicitacoes()

        if not solicitacoes:
            await message.reply_text(
                "Não há solicitações de vínculo no momento."
            )
            return

        text, keyboard = create_page(solicitacoes, page=0)

        await message.reply_text(text, reply_markup=keyboard)

    @app.on_callback_query(filters.regex(r"^solicitacoes:(\d+)$"))
    async def solicitacoes_page(client: Client, callback_query: CallbackQuery):
        solicitacoes = await get_solicitacoes()

        page = int(callback_query.data.split(":")[1])

        text, keyboard = create_page(solicitacoes, page)

        await callback_query.message.edit_text(text, reply_markup=keyboard)

        await callback_query.answer()

if __name__ == '__main__':
    pass