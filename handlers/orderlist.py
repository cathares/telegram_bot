from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    FSInputFile, CallbackQuery
)

import emoji

from states import Form
router = Router()


@router.callback_query(F.data == "toOrderList")
async def about_command_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.orderList)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        text="Мои заказы:...",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Command("my_orders"))
async def about_command_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.orderList)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        text="Мои заказы:...",
        reply_markup=builder.as_markup()
    )
