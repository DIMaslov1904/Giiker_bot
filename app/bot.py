import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher

from config_reader import config
from storage import storage
from handlers import common, game


async def main():
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    storage.setting(storage_time=300, bot=bot)  # временное хранилище на 5 минут
    storage.start()

    dp.include_routers(
        common.router,
        game.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')

