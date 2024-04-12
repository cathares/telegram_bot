from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    CallbackQuery
)

from config import STATUS_LIST, my_orders_text_template
from db.database import db

import emoji

from states import Form

router = Router()


@router.callback_query(F.data == "toOrderList")
async def my_orders_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.orderList)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("В обработке"),
            callback_data='accepted'
        ),
        InlineKeyboardButton(
            text=emoji.emojize("В пути"),
            callback_data='delievering'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Доставлено"),
            callback_data='delievered'
        ),
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        text="Выберите статус заказа",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Command("my_orders"))
async def my_orders_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.orderList)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(emoji.emojize("В обработке")),
            callback_data='accepted'
        ),
        InlineKeyboardButton(
            text=emoji.emojize(emoji.emojize("В пути")),
            callback_data='delievering'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Доставлено"),
            callback_data='delieverd'
        ),
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        text="Выберите статус заказа",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.in_({'delievered', 'delievering', 'accepted'}))
async def orderlist_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.orderList)
    cur = db.cursor()
    data = cur.execute(
        f"SELECT * FROM orders WHERE user_id == {callback.from_user.id} AND status == '{callback.data}' ").fetchall()
    cur.close()
    print(type(data))
    print(data)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toOrderList"
        )
    )
    if not data:
        await callback.message.answer(
            text="Заказов пока нет",
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.answer(
            text="<b>Ваши заказы\n\n</b>" + '\n'.join(emoji.emojize(f"<b>Номер заказа: {data[i][0]}</b>"
                                                                    f"\n🛒Артикул: {data[i][3]} "
                                                                    f"\n📐Размер:"f" {data[i][4]}"
                                                                    f"\n👥ФИО:"f" {data[i][5]}"
                                                                    f"\n☎Номер телефона: {data[i][6]}"
                                                                    f"\n🚛Адрес СДЕКа: {data[i][7]}"
                                                                    f"\n🏷Промокод: {data[i][8] if data[i][8] is not None else ''}"
                                                                    f"\n🕐Статус заказа: {STATUS_LIST[data[i][9]]}\n")
                                                      for i in
                                                      range(0, len(data))),
            parse_mode='HTML',
            reply_markup=builder.as_markup()
        )
    await callback.answer()

