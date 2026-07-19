from pyrogram import Client

from backend.core.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_ID
from backend.messages.handlers import start, register, form_handler, logar
from backend.messages.handlers.user import professores, projetos, universidades, vincular, solicitacao_info
from backend.messages.handlers.admin import solicitacoes_funcs

app = Client(
    name="bot",
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
    bot_token=TELEGRAM_BOT_ID,
    in_memory=True
)

start.register(app)
register.register(app)
form_handler.register(app)
logar.register(app)

professores.register(app)
projetos.register(app)
universidades.register(app)
vincular.register(app)
solicitacao_info.register(app)

solicitacoes_funcs.register(app)

if __name__ == '__main__':
    app.run()