import emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton
)

from states import Form

router = Router()


# ТУТ НАЧИНАЮТСЯ ХЕНДЛЕРЫ НА КАЛЬКУЛЯТОР


@router.message(Command("calc"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.calc)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        "Введите стоимость товара",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "toCalc")
async def back_to_calc_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.calc)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        "Введите стоимость товара",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.calc)
async def delivery_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.calc_delivery)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toCalc"
        )
    )
    await message.answer(
        "Выберите доставку:",
        reply_markup=builder.as_markup()
    )


@router.message(Form.calc_delivery)
async def full_price_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.calc_price)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Назад в меню"),
            callback_data="toStart"
        )
    )
    await message.answer(
        "Итоговая стоимость:",
        reply_markup=builder.as_markup()
    )


'''
@dp.callback_query(Form.check, F.data == "edit")
async def edit(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("Артикул"),
            callback_data="article"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("Размер"),
            callback_data="edit"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("ФИО"),
            callback_data="edit"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("Номер телефона"),
            callback_data="edit"
        )
    )
    await callback.message.answer("Что вы хотите изменить?")
'''
