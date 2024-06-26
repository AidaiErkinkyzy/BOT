from config import TOKEN
import asyncio
from aiogram import Bot, Dispatcher # type: ignore
from handlers.commands import *
import logging
import sys



async def main():

    bot = Bot(token=TOKEN) # Подключает 
    dp = Dispatcher()
    
    setup_routers(dp, bot)

    await dp.start_polling(bot) # запускает бота в активном состоянии


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,stream=sys.stdout)

    try:
        asyncio.run(main())
    except Exception as e:
        print("Ошибка",e)