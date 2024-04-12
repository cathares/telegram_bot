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

from config import admin_ids, STATUS_LIST
from db.database import db
from states import Form

router = Router()


class Newsletter(StatesGroup):
    message = State()


class AdminFilter(Filter):
    async def __call__(self, message: Message):
        cur = db.cursor()
        print(cur.execute("SELECT admin_id FROM admins").fetchall())
        return message.from_user.id in admin_ids


@router.callback_query(AdminFilter(), F.data == "admin")
async def admin_panel(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Рассылка",
            callback_data="ToNewsletter"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Мои заказы",
            callback_data="admin_toOrders"
        )
    )
    await callback.message.answer(
        'Интерфейс администратора',
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "ToNewsletter")
async def newsletter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Newsletter.message)
    await callback.message.answer("Отправьте сообщение для рассылки")
    await callback.answer()


@router.message(AdminFilter(), Newsletter.message)
async def send_newsletter(message: Message, state: FSMContext):
    await message.answer("Подождите, идет отправка...")
    cur = db.cursor()
    users = cur.execute("SELECT user_id from users").fetchall()
    for user in users:
        print(user)
        try:
            await message.send_copy(chat_id=user[0])
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()


@router.callback_query(AdminFilter(), F.data.startswith("admin_order_"))
async def accept_order(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":check_mark_button:Заказ взят"),
            callback_data="NULL"
        )
    )
    order_id = callback.data[12:]
    cur = db.cursor()
    print(callback.data[12:])
    print(cur.execute("SELECT worker FROM orders WHERE order_id=={id}".format(id=order_id)).fetchone())
    if cur.execute("SELECT worker FROM orders WHERE order_id=={id}".format(id=order_id)).fetchone()[0] is None:
        cur.execute(
            "UPDATE orders SET worker={worker} WHERE order_id=={id}".format(worker=callback.from_user.id, id=order_id))
        await callback.message.answer(f"Заказ {order_id} взят пользователем {callback.from_user.first_name}")
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
        db.commit()
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
        text="Выберите пункт меню",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "OrdersInWork")
async def ordersInWork(callback: CallbackQuery):
    cur = db.cursor()
    orders = cur.execute("SELECT * FROM orders WHERE worker == {worker} AND status != 'delievered'".format(
        worker=callback.from_user.id)).fetchall()
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
                f"\n🚛Адрес СДЕКа: {orders[i][7]}"
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
    await callback.message.answer(
        text=f"Выберите статус для заказа {id}",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

''' ПОЧИНИТЬ КОСТЫЛЬ НЕ ЗАБУДЬ'''


@router.callback_query(AdminFilter(), F.data.startswith("status"))
async def change_status(callback: CallbackQuery):
    order_id = callback.data[-2:]
    status = callback.data[7:-3]
    cur = db.cursor()
    cur.execute(f"UPDATE orders SET status='{status}' WHERE order_id =='{order_id}'")
    cur.close()
    await callback.message.edit_text(
        text=f"Статус заказа {order_id} изменен на <b>{STATUS_LIST[status]}</b>",
        parse_mode="HTML"
    )


@router.callback_query(AdminFilter(), F.data == "OrdersInWork")
async def ordersInWork(callback: CallbackQuery):
    cur = db.cursor()
    orders = cur.execute("SELECT * FROM orders WHERE worker == {worker} AND status == 'delievered'".format(
        worker=callback.from_user.id)).fetchall()
    builder = InlineKeyboardBuilder()
    for i in range(0, len(orders)):
        await callback.message.answer(
            text=emoji.emojize(
                f"\nНомер заказа: {orders[i][0]}\n"
                f"Имя пользователя: {orders[i][2]}"
                f"\n🛒Артикул: {orders[i][3]} "
                f"\n📐Размер:"f" {orders[i][4]}"
                f"\n👥ФИО:"f" {orders[i][5]}"
                f"\n☎Номер телефона: {orders[i][6]}"
                f"\n🚛Адрес СДЕКа: {orders[i][7]}"
                f"\n🏷Промокод: {orders[i][8]}"
                f"\n🕐Статус заказа: {STATUS_LIST[orders[i][9]]}"
            ),
            reply_markup=builder.as_markup()
        )
