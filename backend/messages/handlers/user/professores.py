import math

from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from backend.utils.professores_utils import get_professores
from backend.database.models.professor import Professor

PAGE_SIZE = 5

def create_page(professores: List[Professor], page: int):
    total_pages = math.ceil(len(professores) / PAGE_SIZE)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    current = professores[start:end]

    text = "📚 Lista de Professores\n\n"

    for p in current:
        text += f"• {p.user_id} - {p.universidade_id} - {p.departamento}\n"

    text += f"\nPágina {page + 1}/{total_pages}"

    buttons = []
    navigation = []

    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️", callback_data=f"professores:{page - 1}"))

    if page < total_pages - 1:
        navigation.append(InlineKeyboardButton("➡️", callback_data=f"professores:{page + 1}"))

    if navigation:
        buttons.append(navigation)

    keyboard = InlineKeyboardMarkup(buttons) if buttons else None

    return text, keyboard

def register(app: Client):
    @app.on_message(filters.command("professores"))
    async def professores_command(client: Client, message: Message):
        try:
            professores = await get_professores()

            print("Professores encontrados:", professores)

            if not professores:
                await message.reply_text("Não há professores cadastradas.")
                return

            text, keyboard = create_page(professores, page=0)

            await message.reply_text(text, reply_markup=keyboard)
        except Exception as e:
            print("ERRO /professores:", e)

            await message.reply_text(f"Erro ao listar professores:\n{e}")

    @app.on_callback_query(filters.regex(r"^professores:(\d+)$"))
    async def professores_page(client: Client, callback_query: CallbackQuery):
        try:
            professores = await get_professores()

            page = int(callback_query.data.split(":")[1])

            text, keyboard = create_page(professores, page)

            await callback_query.message.edit_text(text, reply_markup=keyboard)

            await callback_query.answer()
        except Exception as e:
            print("ERRO CALLBACK:", e)

            await callback_query.answer("Erro ao trocar página.", show_alert=True)

if __name__ == '__main__':
    pass