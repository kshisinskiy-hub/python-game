import csv
import json
import logging
from pathlib import Path

# Определяем базовую директорию проекта через pathlib
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "recipes.json"
LOG_PATH = BASE_DIR / "game_flight.log"
STATS_PATH = BASE_DIR / "session_stats.csv"

# Настройка модуля logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)


def log_event(message: str, level: str = "info") -> None:
    """Логирование событий с временными метками."""
    if level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    else:
        logging.info(message)


def load_game_config() -> dict:
    """Загрузка конфигурации из JSON с валидацией ошибок."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            log_event("Файл конфигурации recipes.json успешно загружен.")
            return data
    except FileNotFoundError:
        log_event(
            "Файл recipes.json не найден! Загрузка значений по умолчанию.",
            "warning",
        )
    except json.JSONDecodeError:
        log_event(
            "Ошибка структуры JSON в recipes.json! Использование дефолтов.",
            "error",
        )

    # Дефолтное состояние, если файл отсутствует или поврежден
    return {
        "initial_elements": [
            {"type": "fire", "x": 100, "y": 100},
            {"type": "water", "x": 220, "y": 100},
        ],
        "recipes": {"fire+water": "steam"},
    }


def save_session_stats(
    player_name: str, crafted_count: int, play_time_sec: float
) -> None:
    """Сохранение результатов сессии в CSV-файл."""
    file_exists = STATS_PATH.exists() and STATS_PATH.stat().st_size > 0

    try:
        with open(STATS_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Если файл создается впервые, пишем заголовки
            if not file_exists:
                writer.writerow(
                    ["Имя Игрока", "Создано Элементов", "Время (сек)"]
                )

            writer.writerow(
                [player_name, crafted_count, round(play_time_sec, 1)]
            )
            log_event(
                f"Статистика игрока {player_name} успешно записана в CSV."
            )
    except OSError as e:
        log_event(f"Не удалось записать статистику в CSV: {e}", "error")