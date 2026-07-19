import math

from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.utils.user_utils import exists_user_telegram
from backend.utils.administrador_utils import is_user_admin_by_telegram
from backend.utils.solicitacoes_utils import get_solicitacoes

from backend.database.models.solicitacoes_vincular import SolicitacaoVincular
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor

PAGE_SIZE = 3

def create_page(solicitacoes: List[SolicitacaoVincular], page: int):
    total_pages = math.ceil(len(solicitacoes) / PAGE_SIZE)

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    current = solicitacoes[start:end]

    text = "📚 Lista de Solicitaçoes\n\n"

    for solicitacao in current:
        text = (
            "📄 **Solicitação de Vínculo**\n"
            f"ID: {solicitacao.id}\n"
            f"Tipo: {solicitacao.tipo}\n"
            f"Telegram ID: {solicitacao.user_id}\n"
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

def manage_solicitacao(id_solicitacao: int, action: str) -> str:
    db: Session = SessionLocal()

    try:
        if action not in ("aceitar", "recusar"):
            return "Ação inválida."

        solicitacao = db.get(SolicitacaoVincular, id_solicitacao)

        if solicitacao is None:
            return "Solicitação não encontrada."

        if action == "recusar":
            db.delete(solicitacao)
            db.commit()
            return "Solicitação recusada com sucesso."

        tipo = solicitacao.tipo.lower()

        if tipo in ("aluno", "estudante"):

            estudante = Estudante(
                user_id=solicitacao.user_id,
                universidade_id=solicitacao.universidade_id,
                matricula=solicitacao.matricula
            )

            db.add(estudante)

        elif tipo == "professor":

            professor = Professor(
                user_id=solicitacao.user_id,
                universidade_id=solicitacao.universidade_id,
                departamento=solicitacao.departamento
            )

            db.add(professor)

        else:
            return f"Tipo '{solicitacao.tipo}' desconhecido."

        db.delete(solicitacao)

        db.commit()

        return "Solicitação aceita com sucesso."

    except Exception as e:
        db.rollback()
        return f"Erro: {e}"

    finally:
        db.close()

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

        tam = len(message.command)

        if tam == 1:
            solicitacoes = await get_solicitacoes()

            if not solicitacoes:
                await message.reply_text(
                    "Não há solicitações de vínculo no momento."
                )
                return

            text, keyboard = create_page(solicitacoes, page=0)

            await message.reply_text(text, reply_markup=keyboard)

        elif tam == 3:
            comando = message.command[1].lower()
            id_solicitacoes = message.command[2].lower()

            await message.reply_text(manage_solicitacao(int(id_solicitacoes), comando))

        else:
            await message.reply_text(
                "Uso incorreto do comando.\n\n"
                "Para visualizar solicitações: /solicitacoes\n"
                "Para aceitar uma solicitação: /solicitacoes aceitar <id>\n"
                "Para recusar uma solicitação: /solicitacoes recusar <id>"
            )

    @app.on_callback_query(filters.regex(r"^solicitacoes:(\d+)$"))
    async def solicitacoes_page(client: Client, callback_query: CallbackQuery):
        solicitacoes = await get_solicitacoes()

        page = int(callback_query.data.split(":")[1])

        text, keyboard = create_page(solicitacoes, page)

        await callback_query.message.edit_text(text, reply_markup=keyboard)

        await callback_query.answer()

if __name__ == '__main__':
    pass