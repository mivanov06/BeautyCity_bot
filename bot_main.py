import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import BasicAuth

from config_data.config import load_config
from handlers import user_handlers, other_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d | %(levelname)-8s | [%(asctime)s] | '
               '%(name)s | %(message)s'
    )

    logger.info("Starting Bot")
    config = load_config()
    auth = BasicAuth(login='login', password='password')
    # session = AiohttpSession(proxy=('http://proxy.server:3128', auth))
    session = AiohttpSession()

    bot = Bot(config.tg_bot.token, parse_mode="HTML", session=session)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    dp.startup.register(set_main_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def set_main_menu(bot: Bot):
    await bot.set_my_commands(
        [
            types.BotCommand(
                command="/start",
                description="Начало"
            ),
            types.BotCommand(
                command="/help",
                description="Справка по работе бота"
            ),
        ]
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped")
