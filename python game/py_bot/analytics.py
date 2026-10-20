import csv
import io
import json


def parse_and_verify_csv(file_text: str) -> tuple[list[dict], list[str]]:
    """Парсинг и верификация CSV выгрузки игрока[cite: 11, 12]."""
    records = []
    errors = []

    reader = csv.reader(io.StringIO(file_text))
    rows = [row for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        return [], ["Файл пуст"]

    # Пропускаем заголовок, если он есть
    start_idx = (
        1
        if rows[0][0].strip().lower() in ("имя", "name", "имя игрока")
        else 0
    )

    for line_no, row in enumerate(rows[start_idx:], start=start_idx + 1):
        if len(row) < 3:
            errors.append(
                f"Строка {line_no}: ожидается минимум 3 поля (Имя, Создано, Время)"
            )
            continue

        name = row[0].strip()
        try:
            crafted = int(row[1].strip())
            play_time = float(row[2].strip())
        except ValueError:
            errors.append(f"Строка {line_no}: некорректные числовые данные")
            continue

        # Верификация значений[cite: 11, 12]
        if not name:
            errors.append(f"Строка {line_no}: пустое имя")
            continue
        if crafted < 0:
            errors.append(f"Строка {line_no}: отрицательное количество крафтов")
            continue
        if play_time <= 0 or play_time > 86400:
            errors.append(f"Строка {line_no}: нереалистичное время сессии")
            continue

        records.append(
            {"name": name, "crafted": crafted, "play_time": play_time}
        )

    return records, errors


def get_top_capital(records: list[dict], limit: int = 5) -> str:
    """Формирует топ игроков по капиталу (количеству созданных элементов)[cite: 12, 15]."""
    if not records:
        return "📊 Таблица лидеров пуста."

    sorted_records = sorted(
        records, key=lambda x: (-x["crafted"], x["play_time"])
    )[:limit]

    text = "🏆 <b>ТОП АЛХИМИКОВ ПО КАПИТАЛУ</b>\n\n<pre>"
    text += f"{'№':<2} {'Имя':<12} {'Крафты':<7} {'Время':<6}\n"
    text += "-" * 30 + "\n"

    for idx, r in enumerate(sorted_records, 1):
        text += f"{idx:<2} {r['name'][:10]:<12} {r['crafted']:<7} {r['play_time']:>5.1f}s\n"

    text += "</pre>"
    return text


def get_player_stats(records: list[dict], player_name: str) -> str:
    """Статистика игрока по названию[cite: 12, 14]."""
    player_recs = [
        r
        for r in records
        if r["name"].lower() == player_name.strip().lower()
    ]
    if not player_recs:
        return f"🔍 Игрок <b>{player_name}</b> не найден в базе выгрузок."

    total_games = len(player_recs)
    total_crafted = sum(r["crafted"] for r in player_recs)
    best_crafted = max(r["crafted"] for r in player_recs)
    avg_time = sum(r["play_time"] for r in player_recs) / total_games

    return (
        f"👤 <b>Статистика алхимика: {player_name}</b>\n\n"
        f"🎮 Всего сессий: <b>{total_games}</b>\n"
        f"⚗️ Создано элементов: <b>{total_crafted}</b>\n"
        f"⭐ Рекорд за сессию: <b>{best_crafted}</b>\n"
        f"⏱️ Среднее время игры: <b>{avg_time:.1f} сек</b>"
    )


def check_achievements(records: list[dict], player_name: str) -> str:
    """Награды и достижения игрока[cite: 12, 15]."""
    player_recs = [
        r
        for r in records
        if r["name"].lower() == player_name.strip().lower()
    ]
    if not player_recs:
        return f"🔍 Игрок <b>{player_name}</b> не найден."

    total_crafted = sum(r["crafted"] for r in player_recs)
    max_crafted = max(r["crafted"] for r in player_recs)

    achievements = [
        (
            "🌱 Ученик Зельевара",
            "Сделать первый крафт",
            total_crafted >= 1,
        ),
        (
            "🔥 Мастер Элементов",
            "Создать 10+ элементов за всё время",
            total_crafted >= 10,
        ),
        (
            "⚡ Быстрый Алхимик",
            "Создать 5+ элементов за одну сессию",
            max_crafted >= 5,
        ),
        (
            "👑 Великий Архимаг",
            "Создать 50+ элементов",
            total_crafted >= 50,
        ),
    ]

    text = f"🏅 <b>Достижения алхимика {player_name}:</b>\n\n"
    for name, desc, unlocked in achievements:
        status = "✅ Открыто" if unlocked else "🔒 Закрыто"
        text += f"<b>{name}</b> ({status})\n<i>{desc}</i>\n\n"

    return text