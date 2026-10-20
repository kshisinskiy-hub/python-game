import asyncio
import io
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message
from analytics import (
    check_achievements,
    get_player_stats,
    get_top_capital,
    parse_and_verify_csv,
)

from config import BOT_TOKEN, LOG_PATH
from keyboards import back_to_menu_keyboard, main_menu_keyboard, stats_keyboard
from session import get_all_subscribers, load_session, save_session

# Настройка логирования
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Глобальное хранилище спарсенных записей в памяти
GLOBAL_RECORDS = []


# FSM состояния
class BotState(StatesGroup):
    MENU = State()
    WAIT_FILE = State()
    WAIT_NAME = State()


# Управление экранами через edit_text (Антифлуд)
async def show_screen(
    chat_id: int, user_id: int, text: str, reply_markup=None
) -> None:
    session = load_session(user_id)
    screen_id = session.get("screen_message_id")
    screen_chat = session.get("screen_chat_id")

    if screen_id and screen_chat == chat_id:
        try:
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=screen_id,
                reply_markup=reply_markup,
                parse_mode="HTML",
            )
            return
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                return
            logging.info(
                f"Экран {screen_id} недоступен ({e}), отправляем новый"
            )
        except Exception as e:
            logging.info(f"Ошибка редактирования экрана: {e}")

    # Если не удалось отредактировать — отправляем новое
    msg = await bot.send_message(
        chat_id, text, reply_markup=reply_markup, parse_mode="HTML"
    )
    session["screen_message_id"] = msg.message_id
    session["screen_chat_id"] = chat_id
    save_session(user_id, session)


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ЛОГИКИ ---


async def process_top(chat_id: int, user_id: int):
    top_text = get_top_capital(GLOBAL_RECORDS)
    await show_screen(chat_id, user_id, top_text, back_to_menu_keyboard())


async def process_stats(chat_id: int, user_id: int, state: FSMContext):
    session = load_session(user_id)
    if not session.get("player_name"):
        await state.set_state(BotState.WAIT_NAME)
        await show_screen(
            chat_id,
            user_id,
            "⌨️ <b>Введите имя алхимика для поиска:</b>",
            back_to_menu_keyboard(),
        )
    else:
        stats_text = get_player_stats(
            GLOBAL_RECORDS, session.get("player_name")
        )
        await show_screen(
            chat_id, user_id, stats_text, stats_keyboard(has_name=True)
        )


async def process_achievements(chat_id: int, user_id: int, state: FSMContext):
    session = load_session(user_id)
    if not session.get("player_name"):
        await state.set_state(BotState.WAIT_NAME)
        await show_screen(
            chat_id,
            user_id,
            "⌨️ <b>Введите имя алхимика для просмотра наград:</b>",
            back_to_menu_keyboard(),
        )
    else:
        ach_text = check_achievements(
            GLOBAL_RECORDS, session.get("player_name")
        )
        await show_screen(
            chat_id, user_id, ach_text, stats_keyboard(has_name=True)
        )


async def process_upload(chat_id: int, user_id: int, state: FSMContext):
    await state.set_state(BotState.WAIT_FILE)
    text = (
        "📂 <b>Загрузка результатов сессии</b>\n\n"
        "Отправьте CSV-файл с результатами игры (`session_stats.csv`) или файл сохранения `inventory_save.json`."
    )
    await show_screen(chat_id, user_id, text, back_to_menu_keyboard())


async def process_watch(chat_id: int, user_id: int):
    session = load_session(user_id)
    session["subscribed"] = not session.get("subscribed", False)
    save_session(user_id, session)

    status = "включили" if session["subscribed"] else "отключили"
    text = (
        f"🔔 Вы успешно <b>{status}</b> уведомления о новых результатах!\n\n"
        "📜 <b>Главное меню:</b>"
    )
    await show_screen(
        chat_id, user_id, text, main_menu_keyboard(session["subscribed"])
    )


# --- ХЕНДЛЕРЫ КОМАНД (Ввод через слэш) ---


@dp.message(Command("start"))
@dp.message(Command("menu"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(BotState.MENU)
    user_id = message.from_user.id
    session = load_session(user_id)

    text = (
        "🔮 <b>Добро пожаловать в «Лавку Алхимика»!</b>\n\n"
        "Я бот-аналитик игры «Алхимический Рынок». Я анализирую ваши "
        "выгрузки результатов, строю рейтинг и фиксирую достижения!\n\n"
        "<b>Доступные команды:</b>\n"
        "/top — рейтинг по капиталу инвентаря\n"
        "/stats — статистика игрока\n"
        "/achievements — награды\n"
        "/upload — приём и верификация CSV / JSON\n"
        "/watch — подписка на уведомления"
    )
    await show_screen(
        message.chat.id,
        user_id,
        text,
        main_menu_keyboard(session.get("subscribed")),
    )


@dp.message(Command("top"))
async def cmd_top(message: Message, state: FSMContext):
    await state.clear()
    await process_top(message.chat.id, message.from_user.id)


@dp.message(Command("stats"))
async def cmd_stats(message: Message, state: FSMContext):
    await state.clear()
    await process_stats(message.chat.id, message.from_user.id, state)


@dp.message(Command("achievements"))
async def cmd_achievements(message: Message, state: FSMContext):
    await state.clear()
    await process_achievements(message.chat.id, message.from_user.id, state)


@dp.message(Command("upload"))
async def cmd_upload(message: Message, state: FSMContext):
    await state.clear()
    await process_upload(message.chat.id, message.from_user.id, state)


@dp.message(Command("watch"))
async def cmd_watch(message: Message, state: FSMContext):
    await state.clear()
    await process_watch(message.chat.id, message.from_user.id)


# --- CALLBACK ХЕНДЛЕРЫ (Кнопки) ---


@dp.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(BotState.MENU)
    user_id = callback.from_user.id
    session = load_session(user_id)
    await callback.answer()
    await show_screen(
        callback.message.chat.id,
        user_id,
        "📜 <b>Главное меню:</b>",
        main_menu_keyboard(session.get("subscribed")),
    )


@dp.callback_query(F.data == "top")
async def cb_top(callback: CallbackQuery):
    await callback.answer()
    await process_top(callback.message.chat.id, callback.from_user.id)


@dp.callback_query(F.data == "stats")
async def cb_stats(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_stats(
        callback.message.chat.id, callback.from_user.id, state
    )


@dp.callback_query(F.data == "achievements")
async def cb_achievements(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_achievements(
        callback.message.chat.id, callback.from_user.id, state
    )


@dp.callback_query(F.data == "change_name")
async def cb_change_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = callback.from_user.id
    await state.set_state(BotState.WAIT_NAME)
    await show_screen(
        callback.message.chat.id,
        user_id,
        "⌨️ <b>Введите новое имя игрока для поиска:</b>",
        back_to_menu_keyboard(),
    )


@dp.callback_query(F.data == "upload")
async def cb_upload(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_upload(
        callback.message.chat.id, callback.from_user.id, state
    )


@dp.callback_query(F.data == "toggle_sub")
async def cb_toggle_sub(callback: CallbackQuery):
    await callback.answer()
    await process_watch(callback.message.chat.id, callback.from_user.id)


# --- ОБРАБОТКА ВВОДА ДАННЫХ И ФАЙЛОВ ---


@dp.message(StateFilter(BotState.WAIT_NAME))
async def handle_name_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    session = load_session(user_id)
    session["player_name"] = name
    save_session(user_id, session)

    await state.set_state(BotState.MENU)
    stats_text = get_player_stats(GLOBAL_RECORDS, name)
    await show_screen(
        message.chat.id,
        user_id,
        stats_text,
        stats_keyboard(has_name=True),
    )


@dp.message(StateFilter(BotState.WAIT_FILE), F.document)
async def handle_file_upload(message: Message, state: FSMContext):
    user_id = message.from_user.id
    buffer = io.BytesIO()

    # Скачивание файла из Telegram
    await bot.download(message.document, destination=buffer)
    file_text = buffer.getvalue().decode("utf-8-sig", errors="ignore")

    records, errors = parse_and_verify_csv(file_text)

    if records:
        GLOBAL_RECORDS.extend(records)
        logging.info(
            f"Пользователь {user_id} загрузил {len(records)} корректных записей."
        )

        # Рассылка уведомлений подписчикам
        for sub_id in get_all_subscribers():
            if sub_id != user_id:
                try:
                    await bot.send_message(
                        sub_id,
                        f"📢 <b>Новые результаты!</b> Пользователь загрузил {len(records)} записей сессий.",
                        parse_mode="HTML",
                    )
                except Exception:
                    pass

    report = f"✅ <b>Успешно добавлено записей:</b> {len(records)}\n"
    if errors:
        report += (
            f"⚠️ <b>Отклонено строк ({len(errors)}):</b>\n"
            + "\n".join(errors[:3])
        )

    await state.set_state(BotState.MENU)
    await show_screen(
        message.chat.id, user_id, report, back_to_menu_keyboard()
    )


async def main():
    logging.info("Запуск Telegram-бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())