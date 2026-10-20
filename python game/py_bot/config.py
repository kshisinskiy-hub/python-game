import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

LOG_PATH = BASE_DIR / "bot_flight.log"

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "5817786718:AAEB9oIcNzILZo7XAjxGiwaT_H2v_02S0_I")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Telegram ID админа