from pyrogram import Client, filters

def register(app: Client):
    @app.on_message(filters.command("start"))
    def start(client, message):
        message.reply(
            "👋 Olá! Eu sou o bot Orienta.IA.\n\n"
            "Comandos disponíveis:\n"
            "/start - Iniciar\n"
            "/registrar - Registrar telegram na plataforma\n"
        )

if __name__ == '__main__':
    pass