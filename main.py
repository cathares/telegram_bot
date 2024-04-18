import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand

from handlers import order, calc, main_menu, about, orderlist, feedback, admin, settings

# async def on_startup(_):
# await db.db_start()
from start_bot import bot


async def main():
    dp = Dispatcher()
    dp.include_routers(main_menu.router, order.router, calc.router, about.router, orderlist.router, feedback.router, admin.router, settings.router)
    main_commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(command="/new_order", description="Оформить заказ"),
        BotCommand(command="/calc", description="Калькулятор заказа"),
        BotCommand(command="/about", description="О нас"),
        BotCommand(command="/feedback", description="Обратная связь"),
        BotCommand(command="/my_orders", description="Мои заказы"),
    ]
    await bot.set_my_commands(main_commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
