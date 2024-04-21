from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handlers.admin_panel.util import AdminFilter


router = Router()


@router.callback_query(AdminFilter(), F.data == "admin")
async def admin_panel(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Мои заказы",
            callback_data="admin_toOrders"
        ),
        InlineKeyboardButton(
            text="Мои заявки",
            callback_data="admin_toTickets"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Рассылка",
            callback_data="ToNewsletter"
        ),
        InlineKeyboardButton(
            text="Промокоды",
            callback_data="admin_promo"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить настройки",
            callback_data="admin_change_settings"
        )
    )
    await callback.message.answer(
        text='Интерфейс администратора',
        reply_markup=builder.as_markup()
    )
    await callback.answer()
