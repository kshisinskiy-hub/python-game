from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def stats_keyboard(has_name: bool = True) -> InlineKeyboardMarkup:
    rows = []
    if has_name:
        rows.append(
            [InlineKeyboardButton(text="🔄 Сменить имя игрока", callback_data="change_name")]
        )
    rows.append([InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def main_menu_keyboard(is_subscribed: bool = False) -> InlineKeyboardMarkup:
    sub_text = "🔕 Отписаться" if is_subscribed else "🔔 Подписаться"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏆 Топ игроков", callback_data="top"
                ),
                InlineKeyboardButton(
                    text="📊 Моя статистика", callback_data="stats"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏅 Достижения", callback_data="achievements"
                ),
                InlineKeyboardButton(
                    text="📤 Загрузить CSV", callback_data="upload"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=sub_text, callback_data="toggle_sub"
                )
            ],
        ]
    )
    return keyboard


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
        ]
    )