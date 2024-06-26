import re

from aiogram import Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton, CallbackQuery,
)
from handlers.admin_panel.admin_orders import AdminFilter, AdminStates
from db.database import db


router = Router()


@router.callback_query(AdminFilter(), F.data == "admin_change_settings")
async def change_settings(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Изменить курс",
            callback_data="admin_change_rate"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить стоимость доставки",
            callback_data="admin_change_delivery"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить наценку",
            callback_data="admin_change_markup"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin"
        )
    )
    await callback.message.edit_text(
        text="Изменить настройки:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "admin_change_rate")
async def change_rate_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.rate)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin_change_settings"
        )
    )
    cur = db.cursor()
    rate = cur.execute("SELECT rate FROM prices").fetchone()
    await callback.message.edit_text(
        text=f"Текущий курс составляет {rate[0]} руб.\nВведите новый курс:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(AdminFilter(), AdminStates.rate)
async def change_rate_confirm(message: Message, state: FSMContext):
    regex = "[0-9]*[.,]?[0-9]+"
    isDigit = re.findall(regex, message.text)
    if isDigit:
        if re.findall(",", message.text):
            rate = re.sub(",", "..", message.text)
        else:
            rate = message.text
        cur = db.cursor()
        cur.execute(f"UPDATE prices SET rate = '{rate}'")
        db.commit()
        cur.close()
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="В меню",
                callback_data="admin_change_settings"
            )
        )
        await message.answer(
            text=f"Установлен новый курс - {rate} руб.",
            reply_markup=builder.as_markup()
        )
        await state.clear()
    else:
        await message.answer(
            text="Неверный формат. Введите число:",

        )


@router.callback_query(AdminFilter(), F.data == "admin_change_markup")
async def change_markup(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.markup)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin_change_settings"
        )
    )
    cur = db.cursor()
    markup = cur.execute("SELECT markup FROM prices").fetchone()
    cur.close()
    await callback.message.edit_text(
        text=f"Текущая наценка составляет {markup[0]} руб.\nВведите новое значение наценки:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(AdminFilter(), AdminStates.markup)
async def change_rate_confirm(message: Message, state: FSMContext):
    regex = "[0-9]*[.,]?[0-9]+"
    isDigit = re.findall(regex, message.text)
    if isDigit:
        if re.findall(",", message.text):
            markup = re.sub(",", "..", message.text)
        else:
            markup = message.text
        cur = db.cursor()
        cur.execute(f"UPDATE prices SET markup = '{markup}'")
        db.commit()
        cur.close()
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="В меню",
                callback_data="admin_change_settings"
            )
        )
        await message.answer(
            text=f"Установлено новое значение наценки - {markup} руб.",
            reply_markup=builder.as_markup()
        )
        await state.clear()
    else:
        await message.answer(
            text="Неверный формат. Введите число:"
        )


@router.callback_query(AdminFilter(), F.data == "admin_change_delivery")
async def delivery_menu(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Обычная",
            callback_data="usual_delivery"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin_change_settings"
        )
    )
    await callback.message.edit_text(
        text="Выберите доставку:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.endswith("delivery"))
async def change_usual_delivery(callback: CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="admin_change_delivery"
        )
    )
    cur = db.cursor()
    price = cur.execute(f"SELECT usual_delivery FROM prices").fetchone()
    cur.close()
    await state.set_state(AdminStates.usual_delivery)
    await callback.message.edit_text(
        text=f"Текущая стоимость обычной доставки составляет {price[0]} руб.\nВведите новую стоимость:",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()


@router.message(AdminFilter(), AdminStates.usual_delivery)
async def confirm_usual_delivery(message: Message, state: FSMContext):
    regex = "[0-9]*[.,]?[0-9]+"
    isDigit = re.findall(regex, message.text)
    if isDigit:
        if re.findall(",", message.text):
            delivery = re.sub(",", "..", message.text)
        else:
            delivery = message.text
        cur = db.cursor()
        cur.execute(f"UPDATE prices SET usual_delivery = '{delivery}'")
        db.commit()
        cur.close()
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="В меню",
                callback_data="admin_change_settings"
            )
        )
        await message.answer(
            text=f"Установлена новая стоимость обычной доставки - {delivery} руб.",
            reply_markup=builder.as_markup()
        )
        await state.clear()
    else:
        await message.answer(
            text="Неверный формат. Введите число:"
        )
