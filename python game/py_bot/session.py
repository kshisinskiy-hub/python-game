import json
from pathlib import Path
from config import SESSIONS_DIR


def get_session_path(user_id: int) -> Path:
    return SESSIONS_DIR / f"{user_id}.json"


def load_session(user_id: int) -> dict:
    path = get_session_path(user_id)
    if not path.exists():
        return {
            "user_id": user_id,
            "player_name": None,
            "subscribed": False,
            "screen_message_id": None,
            "screen_chat_id": None,
        }
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "user_id": user_id,
            "player_name": None,
            "subscribed": False,
            "screen_message_id": None,
            "screen_chat_id": None,
        }


def save_session(user_id: int, data: dict) -> None:
    path = get_session_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_all_subscribers() -> list[int]:
    """Возвращает список ID пользователей, подписанных на уведомления[cite: 12, 14]."""
    subscribers = []
    for filepath in SESSIONS_DIR.glob("*.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("subscribed"):
                    subscribers.append(data.get("user_id"))
        except Exception:
            continue
    return subscribers