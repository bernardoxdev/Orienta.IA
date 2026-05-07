from pyrogram import Client, filters

from backend.database.connection import SessionLocal
from backend.database.models.user import User

def register(app: Client):
    @app.on_message(filters.command("register"))
    async def start(client, message):
        db = SessionLocal()

        try:
            telegram_id = str(message.from_user.id)

            user = db.query(User).filter(
                User.telegram_id == telegram_id
            ).first()

            if not user:
                user = User(
                    telegram_id=telegram_id,
                    nome=message.from_user.first_name
                )
                db.add(user)
                db.commit()

            await message.reply(
                "Olá! Eu sou o Orienta.IA 🤖"
            )

            await print("Usuarios: " + str(db.query(User).all()))
        finally:
            db.close()

if __name__ == '__main__':
    pass