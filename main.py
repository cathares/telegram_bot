import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand

from handlers import order, calc, main_menu, about, orderlist, feedback
from handlers.admin_panel import admin_menu, admin_settings, admin_feedback, admin_orders, newsletter, promo
from start_bot import bot


async def main():
    dp = Dispatcher()
    dp.include_routers(
        main_menu.router, order.router, calc.router, about.router, orderlist.router, feedback.router,
        admin_menu.router, admin_settings.router, admin_feedback.router, promo.router,
        admin_orders.router, newsletter.router)
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
