import emoji

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton, FSInputFile
)

from config import admin_ids
from middlewares import CheckSubscriptionMiddleware
from states import Form
from db import database as db

router = Router()

router.message.outer_middleware(CheckSubscriptionMiddleware())
router.callback_query.outer_middleware(CheckSubscriptionMiddleware())

@router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.main_menu)
    if message.from_user.username:
        username = f'@{message.from_user.username}'
    else:
        username = message.from_user.first_name
    await db.cmd_start_db(message.from_user.id, username)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("🛒Новый заказ"), callback_data="toArticle"),
        InlineKeyboardButton(text="🧮Калькулятор заказа", callback_data="toCalc"),
    )
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("ℹО нас"), callback_data="toAbout"),
        InlineKeyboardButton(text=emoji.emojize("📲Обратная связь"), callback_data="toFeedback"),
    )
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("📦Мои заказы"), callback_data="toOrderList"),
        InlineKeyboardButton(text=emoji.emojize("📋Отзывы"), url="https://t.me/CHINA_TOWN_Feedback")
    )
    if message.from_user.id in admin_ids:
        builder.row(InlineKeyboardButton(text=emoji.emojize("Панель администратора"), callback_data="admin"))
    await message.answer_photo(
        photo=FSInputFile("content/pic.jpg"),
        caption=f"<b>Вас приветствует CHINA TOWN!\nПоддержка - @CHINA_TOWN_ADMIN</b>",
        parse_mode='HTML',
        reply_markup=builder.as_markup()
    )


@router.callback_query(StateFilter(Form.article, Form.check, Form.calc, None, Form), F.data.in_({"toStart", "cancel"}))
async def back_to_start_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.main_menu)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("🛒Новый заказ"), callback_data="toArticle"),
        InlineKeyboardButton(text=emoji.emojize("🧮Калькулятор заказа"), callback_data="toCalc"),
    )
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("ℹО нас"), callback_data="toAbout"),
        InlineKeyboardButton(text=emoji.emojize("📲Обратная связь"), callback_data="toFeedback"),
    )
    builder.row(
        InlineKeyboardButton(text=emoji.emojize("📦Мои заказы"), callback_data="toOrderList"),
        InlineKeyboardButton(text=emoji.emojize("📋Отзывы"), url="https://t.me/CHINA_TOWN_Feedback")
    )
    if callback.from_user.id in admin_ids:
        builder.row(InlineKeyboardButton(text=emoji.emojize("Панель администратора"), callback_data="admin"))
    await callback.message.answer_photo(
        photo=FSInputFile("content/pic.jpg"),
        caption=f"<b>Вас приветствует CHINA TOWN!\nПоддержка - @CHINA_TOWN_ADMIN</b>",
        parse_mode='HTML',
        reply_markup=builder.as_markup()
    )
    await callback.answer()
