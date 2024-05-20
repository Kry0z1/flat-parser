import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.bot_stuff.handlers import handlers_welcome, handlers_parameters_changing


def get_token(path='./token.txt'):
    with open(path, 'r') as file:
        return file.readline()


async def main():
    logging.basicConfig(level=logging.INFO)
    token = get_token()
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(handlers_welcome.router, handlers_parameters_changing.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
