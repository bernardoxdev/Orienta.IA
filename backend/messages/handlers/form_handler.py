from pyrogram import Client, filters
from pyrogram.types import Message

from passlib.context import CryptContext

from backend.utils.telegram_state_utils import set_state, get_state, clear_state
from backend.utils.user_utils import criar_usuario, get_user_by_telegram_id
from backend.utils.register_utils import register_infos
from backend.utils.universidade_utils import get_universidade_by_nome_ou_sigla
from backend.utils.solicitacoes_utils import gerar_solicitacao
from backend.utils.register_utils import realizar_login

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def register(app: Client):
    @app.on_message(filters.text & ~filters.command(["start", "register", "logar", "professores", "projetos", "universidades", "vincular", "solicitacao_info", "solicitacoes"]))
    async def form_handler(client: Client, message: Message):
        telegram_id = str(message.from_user.id)
        state = get_state(telegram_id)

        if not state:
            return

        # Registrando
        if state == "esperando_nome":
            register_infos[telegram_id]["nome"] = message.text
            set_state(telegram_id, "esperando_username")

            await message.reply("Agora envie um username:")
            return

        if state == "esperando_username":
            register_infos[telegram_id]["username"] = message.text
            set_state(telegram_id, "esperando_email")

            await message.reply_text("Agora envie seu email: ")
            return

        if state == "esperando_email":
            register_infos[telegram_id]["email"] = message.text
            set_state(telegram_id, "esperando_senha")

            await message.reply("Agora envie sua senha:")
            return

        if state == "esperando_senha":
            register_infos[telegram_id]["senha"] = message.text
            data = register_infos[telegram_id]

            await criar_usuario(
                telegram_id=telegram_id,
                username=data["username"],
                nome=data["nome"],
                email=data["email"],
                senha=pwd_context.hash(data["senha"])
            )

            clear_state(telegram_id)
            register_infos.pop(telegram_id, None)

            await message.reply("Registro realizado com sucesso!")
            return

        # Logar
        if state == "esperando_email_logar":
            register_infos[telegram_id]["email"] = message.text
            set_state(telegram_id, "esperando_senha_logar")

            await message.reply("Agora envie sua senha:")
            return

        if state == "esperando_senha_logar":
            register_infos[telegram_id]["senha"] = message.text
            data = register_infos[telegram_id]

            if realizar_login(telegram_id, data["email"], data["senha"]):
                await message.reply("Login realizado com sucesso!")
            else:
                await message.reply("Email ou senha incorretos. Tente novamente.")

            clear_state(telegram_id)
            register_infos.pop(telegram_id, None)

            return

        # Professor
        if state == "esperando_vinculo_professor":
            universidade = await get_universidade_by_nome_ou_sigla(message.text.strip())

            if not universidade:
                await message.reply(
                    "Universidade inválida.\n"
                    "Envie novamente a SIGLA ou NOME da universidade."
                )
                return

            register_infos[telegram_id]["universidade_id"] = universidade.id
            register_infos[telegram_id]["universidade_nome"] = universidade.nome

            set_state(telegram_id, "esperando_departamento_professor")

            await message.reply(
                f"Universidade encontrada: {universidade.nome}\n\n"
                "Agora envie o departamento:"
            )
            return

        if state == "esperando_departamento_professor":
            register_infos[telegram_id]["departamento"] = message.text.strip()
            register_infos[telegram_id]["user_id"] = get_user_by_telegram_id(telegram_id).id
            data = register_infos[telegram_id]

            await gerar_solicitacao(data)

            clear_state(telegram_id)
            register_infos.pop(telegram_id, None)

            await message.reply_text("Voce foi vinculado como professor com sucesso!")
            return

        # Aluno
        if state == "esperando_vinculo_aluno":
            universidade = await get_universidade_by_nome_ou_sigla(message.text.strip())

            if not universidade:
                await message.reply(
                    "Universidade inválida.\n"
                    "Envie novamente a SIGLA ou NOME da universidade."
                )
                return

            register_infos[telegram_id]["universidade_id"] = universidade.id
            register_infos[telegram_id]["universidade_nome"] = universidade.nome

            set_state(telegram_id, "esperando_matricula_aluno")

            await message.reply(
                f"Universidade encontrada: {universidade.nome}\n\n"
                "Agora envie sua matrícula:"
            )
            return

        if state == "esperando_matricula_aluno":
            register_infos[telegram_id]["matricula"] = message.text.strip()
            register_infos[telegram_id]["user_id"] = get_user_by_telegram_id(telegram_id).id
            data = register_infos[telegram_id]
            data.pop("universidade_nome", None)

            await gerar_solicitacao(data)

            clear_state(telegram_id)
            register_infos.pop(telegram_id, None)

            await message.reply_text("Voce foi vinculado como aluno com sucesso!")
            return

if __name__ == '__main__':
    pass