import asyncio
from aiogram import Bot
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    me = await bot.get_me()
    print(f"Успешное подключение! Имя бота: @{me.username}")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())