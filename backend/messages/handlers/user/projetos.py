import math

from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from backend.utils.projetos_utils import get_projetos
from backend.database.models.projetos import Projetos

PAGE_SIZE = 5

def create_page(projetos: List[Projetos], page: int):
    total_pages = math.ceil(len(projetos) / PAGE_SIZE)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    current = projetos[start:end]

    text = "📚 Lista de Projetos\n\n"

    for p in current:
        text += f"• {p.titulo} - {p.descricao}\n"

    text += f"\nPágina {page + 1}/{total_pages}"

    buttons = []
    navigation = []

    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️", callback_data=f"projetos:{page - 1}"))

    if page < total_pages - 1:
        navigation.append(InlineKeyboardButton("➡️", callback_data=f"projetos:{page + 1}"))

    if navigation:
        buttons.append(navigation)

    keyboard = InlineKeyboardMarkup(buttons) if buttons else None

    return text, keyboard

def register(app: Client):
    @app.on_message(filters.command("projetos"))
    async def projetos_command(client: Client, message: Message):
        try:
            projetos = await get_projetos()

            print("Projetos encontradas:", projetos)

            if not projetos:
                await message.reply_text("Não há projetos cadastradas.")
                return

            text, keyboard = create_page(projetos, page=0)

            await message.reply_text(text, reply_markup=keyboard)
        except Exception as e:
            print("ERRO /projetos:", e)

            await message.reply_text(f"Erro ao listar projetos:\n{e}")

    @app.on_callback_query(filters.regex(r"^projetos:(\d+)$"))
    async def projetos_page(client: Client, callback_query: CallbackQuery):
        try:
            projetos = await get_projetos()

            page = int(callback_query.data.split(":")[1])

            text, keyboard = create_page(projetos, page)

            await callback_query.message.edit_text(text, reply_markup=keyboard)

            await callback_query.answer()
        except Exception as e:
            print("ERRO CALLBACK:", e)

            await callback_query.answer("Erro ao trocar página.", show_alert=True)

if __name__ == '__main__':
    pass