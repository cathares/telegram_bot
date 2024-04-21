import emoji
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

data = {}


@router.callback_query(AdminFilter(), F.data == "admin_promo")
async def promocode_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить промокод",
            callback_data="add_promo"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Активные промокоды",
            callback_data="active_promo"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="admin"
        )
    )
    await callback.message.answer(
        text="Промокоды",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "add_promo")
async def add_promo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.admin_promo)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="admin_promo"
        )
    )
    await callback.message.answer(
        "Введите промокод:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(AdminFilter(), AdminStates.admin_promo)
async def add_promo_quant(message: Message, state: FSMContext):
    await state.set_state(AdminStates.admin_promo_quant)
    data.update({message.from_user.id: message.text})
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="add_promo"
        )
    )
    await message.answer(
        "Введите количество использований:",
        reply_markup=builder.as_markup()
    )


@router.message(AdminFilter(), AdminStates.admin_promo_quant)
async def confirm_promo(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="admin_promo"
        )
    )
    await state.clear()
    cur = db.cursor()
    cur.execute(f"INSERT INTO promo (text, quantity) VALUES (?,?)", (data[message.from_user.id], message.text))
    db.commit()
    cur.close()
    data.pop(message.from_user.id)
    await message.answer(text=emoji.emojize("Промокод добавлен"), reply_markup=builder.as_markup())


@router.callback_query(AdminFilter(), F.data == "active_promo")
async def active_promo(callback: CallbackQuery):
    cur = db.cursor()
    promocodes = cur.execute(f"SELECT * FROM promo").fetchall()
    if not promocodes:
        await callback.message.answer(
            text="Промокодов нет"
        )
    else:
        for i in range(0, len(promocodes)):
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(
                    text="Изменить количество использований",
                    callback_data=f"change_quant_{promocodes[i][0]}"
                )
            )
            builder.row(
                InlineKeyboardButton(
                    text="Удалить промокод",
                    callback_data=f"delete_promo_{promocodes[i][0]}"
                )
            )
            await callback.message.answer(
                text=f"Промкод: {promocodes[i][1]}\nОставшееся количество использований: {promocodes[i][2]}",
                reply_markup=builder.as_markup()
            )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.startswith("delete_promo_"))
async def delete_promo(callback: CallbackQuery):
    cur = db.cursor()
    promo = cur.execute(f"SELECT text FROM promo where id == '{callback.data[13:]}'").fetchone()[0]
    cur.execute(f"DELETE FROM promo WHERE id == '{callback.data[13:]}'")
    db.commit()
    await callback.message.edit_text(
        text=f"Промокод {promo} удален"
    )
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.startswith("change_quant_"))
async def change_promo_quant(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.change_promo_quant)
    data.update({callback.from_user.id: callback.data[13:]})
    await callback.message.answer(
        text=f"Введите новое количество использований:"
    )
    await callback.answer()


@router.message(AdminFilter(), AdminStates.change_promo_quant)
async def confirm_quant(message: Message, state: FSMContext):
    await state.clear()
    cur = db.cursor()
    promo = cur.execute(f"SELECT text FROM promo WHERE id == '{data[message.from_user.id]}'").fetchone()[0]
    cur.execute(f"UPDATE promo SET quantity = {message.text} WHERE id == '{data[message.from_user.id]}'")
    db.commit()
    cur.close()
    data.pop(message.from_user.id)
    await message.answer(text=emoji.emojize(f"Количество использований промокода {promo} изменено"))