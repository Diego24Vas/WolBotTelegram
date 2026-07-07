import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN no está definido en .env")

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot.db")
