import math

from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from backend.utils.universidade_utils import get_universidades
from backend.database.models.universidade import Universidade

PAGE_SIZE = 5

def create_page(universidades: List[Universidade], page: int):
    total_pages = math.ceil(len(universidades) / PAGE_SIZE)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    current = universidades[start:end]

    text = "📚 Lista de Universidades\n\n"

    for u in current:
        text += f"• {u.nome}\n"

    text += f"\nPágina {page + 1}/{total_pages}"

    buttons = []
    navigation = []

    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️", callback_data=f"universidades:{page - 1}"))

    if page < total_pages - 1:
        navigation.append(InlineKeyboardButton("➡️", callback_data=f"universidades:{page + 1}"))

    if navigation:
        buttons.append(navigation)

    keyboard = InlineKeyboardMarkup(buttons) if buttons else None

    return text, keyboard

def register(app: Client):
    @app.on_message(filters.command("universidades"))
    async def universidades_command(client: Client, message: Message):
        try:
            universidades = await get_universidades()

            print("Universidades encontradas:", universidades)

            if not universidades:
                await message.reply_text("Não há universidades cadastradas.")
                return

            text, keyboard = create_page(universidades, page=0)

            await message.reply_text(text, reply_markup=keyboard)
        except Exception as e:
            print("ERRO /universidades:", e)

            await message.reply_text(f"Erro ao listar universidades:\n{e}")

    @app.on_callback_query(filters.regex(r"^universidades:(\d+)$"))
    async def universidades_page(client: Client, callback_query: CallbackQuery):
        try:
            universidades = await get_universidades()

            page = int(callback_query.data.split(":")[1])

            text, keyboard = create_page(universidades, page)

            await callback_query.message.edit_text(text, reply_markup=keyboard)

            await callback_query.answer()
        except Exception as e:
            print("ERRO CALLBACK:", e)

            await callback_query.answer("Erro ao trocar página.", show_alert=True)

if __name__ == '__main__':
    pass