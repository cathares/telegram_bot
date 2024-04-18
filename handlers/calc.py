import re

import emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton
)

from db.database import db
from states import Form

router = Router()

prices = {}


# ТУТ НАЧИНАЮТСЯ ХЕНДЛЕРЫ НА КАЛЬКУЛЯТОР


@router.message(Command("calc"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.calc)
    prices.update({message.from_user.id: None})
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        "Введите стоимость товара в CNY (Китайский Юань):",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "toCalc")
async def back_to_calc_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.calc)
    prices.update({callback.from_user.id: None})
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        "Введите стоимость товара в CNY (Китайский Юань):",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.calc)
async def delivery_handler(message: Message, state: FSMContext) -> None:
    regex = "([0-9]*[.,])?[0-9]+"
    isDigit = re.findall(regex, message.text)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toCalc"
        )
    )
    if isDigit:
        await state.set_state(Form.calc_delivery)
        prices[message.from_user.id] = message.text
        innerBuilder = InlineKeyboardBuilder()
        innerBuilder.row(
            InlineKeyboardButton(
                text="Обычная",
                callback_data='usual'
            )
        )
        innerBuilder.row(
            InlineKeyboardButton(
                text=emoji.emojize("⬅Назад"),
                callback_data="toCalc"
            )
        )
        await message.answer(
            "Выберите доставку:",
            reply_markup=innerBuilder.as_markup()
        )
    else:
        await message.answer(
            text="Некорректная стоимость. Введите число:",
            reply_markup=builder.as_markup()
        )


@router.callback_query(Form.calc_delivery)
async def full_price_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.calc_price)
    cur = db.cursor()
    rate = (cur.execute(f"SELECT rate FROM prices").fetchone())[0]
    delivery = (cur.execute(f"SELECT {callback.data + '_delivery'} FROM prices").fetchone())[0]
    markup = (cur.execute(f"SELECT markup FROM prices").fetchone())[0]
    cost = int(prices[callback.from_user.id])*int(rate) + int(delivery) + int(markup)
    prices.pop(callback.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Назад в меню"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        f"Итоговая стоимость: <b>{cost} руб.</b>",
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )
    await callback.answer()
