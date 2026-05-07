import os

from dotenv import load_dotenv

try:
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_BOT_ID = os.getenv('TELEGRAM_BOT_ID')

DATABASE_URL = os.getenv("DATABASE_URL")

if __name__ == '__main__':
    pass