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

from start_bot import bot
from states import Form

router = Router()

data_dict = {}


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
        for i in range(0, len(data)):
            if STATUS_LIST[data[i][9]] == 'В обработке':
                builder = InlineKeyboardBuilder()
                builder.row(
                    InlineKeyboardButton(
                        text="Отменить заказ",
                        callback_data=f"delete_order_{data[i][0]}"
                    )
                )
                await callback.message.answer(
                    text=emoji.emojize(f"<b>Номер заказа: {data[i][0]}</b>"
                                       f"\n🛒Артикул: {data[i][3]} "
                                       f"\n📐Размер:"f" {data[i][4]}"
                                       f"\n👥ФИО:"f" {data[i][5]}"
                                       f"\n☎Номер телефона: {data[i][6]}"
                                       f"\n🚛Адрес СДЭКа: {data[i][7]}"
                                       f"\n🏷Промокод: {data[i][8] if data[i][8] is not None else ''}"
                                       f"\n🕐Статус заказа: {STATUS_LIST[data[i][9]]}\n"),
                    parse_mode='HTML',
                    reply_markup=builder.as_markup()
                )
            else:
                await callback.message.answer(
                    text=emoji.emojize(f"<b>Номер заказа: {data[i][0]}</b>"
                                       f"\n🛒Артикул: {data[i][3]} "
                                       f"\n📐Размер:"f" {data[i][4]}"
                                       f"\n👥ФИО:"f" {data[i][5]}"
                                       f"\n☎Номер телефона: {data[i][6]}"
                                       f"\n🚛Адрес СДЭКа: {data[i][7]}"
                                       f"\n🏷Промокод: {data[i][8] if data[i][8] is not None else ''}"
                                       f"\n🕐Статус заказа: {STATUS_LIST[data[i][9]]}\n"),
                    parse_mode='HTML')
    await callback.answer()


@router.callback_query(F.data.startswith("delete_order_"))
async def delete_order(callback: CallbackQuery):
    order_id = callback.data[13:]
    cur = db.cursor()
    data = cur.execute(f"SELECT * FROM orders WHERE order_id == {order_id}").fetchall()
    cur.execute(f"UPDATE orders SET status = 'canceled' WHERE order_id == {order_id}")
    if data[0][10] is not None:
        admin = data[0][10]
    else:
        admin = ""
    db.commit()
    cur.close()
    await callback.message.answer(
        text="Заказ отменён.",
    )
    await callback.message.delete()
    await callback.answer()
    await bot.send_message(
        chat_id=-4168941250,
        reply_to_message_id=int(data[0][11]),
        text=f"Заказ {order_id} отменён пользователем."
    )
    await bot.send_message(
        chat_id=-4150560440,
        text=emoji.emojize(f"Заказ отменён пользователем."
                           f"\n<b>Номер заказа: {data[0][0]}</b>"
                           f"\nПользователь: {data[0][2]}"
                           f"\n🛒Артикул: {data[0][3]} "
                           f"\n📐Размер:"f" {data[0][4]}"
                           f"\n👥ФИО:"f" {data[0][5]}"
                           f"\n☎Номер телефона: {data[0][6]}"
                           f"\n🚛Адрес СДЭКа: {data[0][7]}"
                           f"\n🏷Промокод: {data[0][8] if data[0][8] is not None else ''}"
                           f"\n🕐Статус заказа: Отменён\n"),
        parse_mode='HTML')
