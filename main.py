import asyncio
import logging
import sys
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import order, calc, main_menu, about, orderlist, feedback


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(main_menu.router, order.router, calc.router, about.router, orderlist.router, feedback.router)
    main_commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(command="/new_order", description="Оформить заказ"),
        BotCommand(command="/calc", description="Калькулятор заказа"),
        BotCommand(command="/about", description="О нас"),
        BotCommand(command="/feedback", description="Обратная связь"),
        BotCommand(command="/my_orders", description="Мои заказы"),
    ]
    await bot.set_my_commands(main_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
