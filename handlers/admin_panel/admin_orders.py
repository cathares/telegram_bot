import re

from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton, CallbackQuery,
)
import emoji

from handlers.admin_panel.util import AdminStates, AdminFilter
from start_bot import bot
from config import STATUS_LIST, TICKETS_STATUS_LIST
from db.database import db

router = Router()


@router.callback_query(AdminFilter(), F.data.startswith("admin_order_"))
async def accept_order(callback: CallbackQuery):
    if callback.from_user.username is not None:
        worker_username = '@' + callback.from_user.username
    else:
        worker_username = callback.from_user.first_name
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":check_mark_button:Заказ взят"),
            callback_data="NULL"
        )
    )
    order_id = callback.data[12:]
    cur = db.cursor()
    if cur.execute("SELECT worker FROM orders WHERE order_id=={id}".format(id=order_id)).fetchone()[0] is None:
        cur.execute(
            "UPDATE orders SET worker={worker}, message_id = {message_id} WHERE order_id=={id}".format(
                worker=callback.from_user.id,
                message_id=callback.message.message_id,
                id=order_id
            )
        )
        db.commit()
        order = cur.execute("SELECT * from orders WHERE order_id == {id}".format(id=order_id)).fetchall()
        if callback.from_user.username:
            username = f'@{callback.from_user.username}'
        else:
            username = callback.from_user.first_name
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
        await callback.message.edit_text(
            text=emoji.emojize(f"Админ: {username}"
                               f"\nНомер заказа: {order[0][0]}"
                               f"\nИмя пользователя: {order[0][2]}"
                               f"\n🛒Артикул: {order[0][3]} "
                               f"\n📐Размер:"f" {order[0][4]}"
                               f"\n👥ФИО:"f" {order[0][5]}"
                               f"\n☎Номер телефона: {order[0][6]}"
                               f"\n🚛Адрес СДЭКа: {order[0][7]}"
                               f"\n🏷Промокод: {order[0][8]}"
                               f"\n🕐Статус заказа: {STATUS_LIST[order[0][9]]}")
        )
    else:
        pass
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "NULL")
async def skip_update(callback: CallbackQuery):
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "admin_toOrders")
async def admin_orders(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Заказы в работе",
            callback_data="OrdersInWork"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Завершенные заказы",
            callback_data="FinishedOrders"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin"
        )
    )
    await callback.message.answer(
        text="<b>Мои заказы</b>",
        parse_mode='HTML',
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "OrdersInWork")
async def ordersInWork(callback: CallbackQuery):
    cur = db.cursor()
    orders = cur.execute("SELECT * FROM orders WHERE worker == {worker} AND status != 'delievered' AND status != 'canceled'".format(
        worker=callback.from_user.id)).fetchall()
    await callback.message.answer(text="Заказы в работе:")
    for i in range(0, len(orders)):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Изменить статус заказа",
                callback_data=f"ChangeStatus_{orders[i][0]}"
            )
        )
        await callback.message.answer(
            text=emoji.emojize(
                f"\nНомер заказа: {orders[i][0]}\n"
                f"Имя пользователя: {orders[i][2]}"
                f"\n🛒Артикул: {orders[i][3]} "
                f"\n📐Размер:"f" {orders[i][4]}"
                f"\n👥ФИО:"f" {orders[i][5]}"
                f"\n☎Номер телефона: {orders[i][6]}"
                f"\n🚛Адрес СДЭКа: {orders[i][7]}"
                f"\n🏷Промокод: {orders[i][8]}"
                f"\n🕐Статус заказа: {STATUS_LIST[orders[i][9]]}"
            ),
            reply_markup=builder.as_markup()
        )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.startswith("ChangeStatus"))
async def changeStatusMenu(callback: CallbackQuery):
    id = callback.data[13:]
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="В обработке",
            callback_data=f"status_accepted_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="В пути",
            callback_data=f"status_delievering_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Доставлен",
            callback_data=f"status_delievered_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Отменить",
            callback_data=f"status_canceled_{id}"
        )
    )
    cur = db.cursor()
    order = cur.execute("SELECT * from orders WHERE order_id == {id}".format(id=id)).fetchall()
    cur.close()
    await callback.message.edit_text(
        text=emoji.emojize(
            f"Выберите статус для заказа {id}\n"
            f"\nНомер заказа: {order[0][0]}"
            f"\nИмя пользователя: {order[0][2]}"
            f"\n🛒Артикул: {order[0][3]} "
            f"\n📐Размер:"f" {order[0][4]}"
            f"\n👥ФИО:"f" {order[0][5]}"
            f"\n☎Номер телефона: {order[0][6]}"
            f"\n🚛Адрес СДЭКа: {order[0][7]}"
            f"\n🏷Промокод: {order[0][8]}"
            f"\n🕐Статус заказа: {STATUS_LIST[order[0][9]]}"
        ),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.startswith("status"))
async def change_status(callback: CallbackQuery):
    if callback.from_user.username:
        username = f'@{callback.from_user.username}'
    else:
        username = callback.from_user.first_name
    status = re.search("(_[a-z]+_)", callback.data).group()[1:-1]
    order_id = re.search("(_\d+)", callback.data).group()[1:]
    cur = db.cursor()
    cur.execute(f"UPDATE orders SET status='{status}' WHERE order_id =='{order_id}'")
    db.commit()
    order = cur.execute("SELECT * from orders WHERE order_id == {id}".format(id=order_id)).fetchall()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Изменить статус заказа",
            callback_data=f"ChangeStatus_{order_id}"
        )
    )
    await callback.message.edit_text(
        text=f"\nНомер заказа: {order[0][0]}"
             f"\nИмя пользователя: {order[0][2]}"
             f"\n🛒Артикул: {order[0][3]} "
             f"\n📐Размер:"f" {order[0][4]}"
             f"\n👥ФИО:"f" {order[0][5]}"
             f"\n☎Номер телефона: {order[0][6]}"
             f"\n🚛Адрес СДЭКа: {order[0][7]}"
             f"\n🏷Промокод: {order[0][8]}"
             f"\n🕐Статус заказа: {STATUS_LIST[order[0][9]]}",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await bot.send_message(
        chat_id=order[0][1],
        text=f"Статус вашего заказа №{order_id} изменен на <b>{STATUS_LIST[order[0][9]]}</b>",
        parse_mode='HTML'
    )
    if STATUS_LIST[order[0][9]] == 'В пути':
        msg = await bot.send_message(
            chat_id=-4161913833,
            text=emoji.emojize(f"Админ: {username}"
                               f"\nНомер заказа: {order[0][0]}"
                               f"\nИмя пользователя: {order[0][2]}"
                               f"\n🛒Артикул: {order[0][3]} "
                               f"\n📐Размер:"f" {order[0][4]}"
                               f"\n👥ФИО:"f" {order[0][5]}"
                               f"\n☎Номер телефона: {order[0][6]}"
                               f"\n🚛Адрес СДЭКа: {order[0][7]}"
                               f"\n🏷Промокод: {order[0][8]}"
                               f"\n🕐Статус заказа: {STATUS_LIST[order[0][9]]}"),
        )
        await bot.delete_message(chat_id=-4168941250, message_id=order[0][11])
        cur.execute(f"UPDATE orders SET message_id='{msg.message_id}' WHERE order_id =='{order_id}'")
        db.commit()
    if STATUS_LIST[order[0][9]] == 'Доставлен':
        await bot.send_message(
            chat_id=-4105238759,
            text=emoji.emojize(f"Админ: {username}"
                               f"\nНомер заказа: {order[0][0]}"
                               f"\nИмя пользователя: {order[0][2]}"
                               f"\n🛒Артикул: {order[0][3]} "
                               f"\n📐Размер:"f" {order[0][4]}"
                               f"\n👥ФИО:"f" {order[0][5]}"
                               f"\n☎Номер телефона: {order[0][6]}"
                               f"\n🚛Адрес СДЭКа: {order[0][7]}"
                               f"\n🏷Промокод: {order[0][8]}"
                               f"\n🕐Статус заказа: {STATUS_LIST[order[0][9]]}"),
        )
        await bot.delete_message(chat_id=-4161913833, message_id=order[0][11])
    if STATUS_LIST[order[0][9]] == 'Отменён':
        await bot.send_message(
            chat_id=-4168941250,
            reply_to_message_id=int(order[0][11]),
            text=f"Заказ {order_id} отменён админом."
        )
        await bot.send_message(
            chat_id=-4150560440,
            text=emoji.emojize(f"Заказ отменён админом."
                               f"\nАдмин: {username}"
                               f"\nПользователь: {order[0][2]}"
                               f"\n<b>Номер заказа: {order[0][0]}</b>"
                               f"\n🛒Артикул: {order[0][3]} "
                               f"\n📐Размер:"f" {order[0][4]}"
                               f"\n👥ФИО:"f" {order[0][5]}"
                               f"\n☎Номер телефона: {order[0][6]}"
                               f"\n🚛Адрес СДЭКа: {order[0][7]}"
                               f"\n🏷Промокод: {order[0][8] if order[0][8] is not None else ''}"
                               f"\n🕐Статус заказа: Отменён\n"),
            parse_mode='HTML')
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "FinishedOrders")
async def ordersInWork(callback: CallbackQuery):
    cur = db.cursor()
    orders = cur.execute("SELECT * FROM orders WHERE worker == {worker} AND status == 'delievered'".format(
        worker=callback.from_user.id)).fetchall()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin_toOrders"
        )
    )
    await callback.message.answer(
        text="Завершенные заказы:",
        reply_markup=builder.as_markup()
    )
    for i in range(0, len(orders)):
        await callback.message.answer(
            text=emoji.emojize(
                f"\nНомер заказа: {orders[i][0]}\n"
                f"Имя пользователя: {orders[i][2]}"
                f"\n🛒Артикул: {orders[i][3]} "
                f"\n📐Размер:"f" {orders[i][4]}"
                f"\n👥ФИО:"f" {orders[i][5]}"
                f"\n☎Номер телефона: {orders[i][6]}"
                f"\n🚛Адрес СДЭКа: {orders[i][7]}"
                f"\n🏷Промокод: {orders[i][8]}"
                f"\n🕐Статус заказа: {STATUS_LIST[orders[i][9]]}"
            ),
        )
    await callback.answer()
