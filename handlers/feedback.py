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

from db.database import db
from start_bot import bot
from states import Form

router = Router()

data = {}


@router.callback_query(F.data == "toFeedback")
async def about_command_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.feedback)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оставить заявку",
            callback_data="toMessage"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Написать саппорту",
            url="t.me/CHINA_TOWN_ADMIN"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="В меню",
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        text="Выберите пункт меню",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Command("feedback"))
async def about_command_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.feedback)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Оставить заявку",
            callback_data="toMessage"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Написать саппорту",
            url="t.me/CHINA_TOWN_ADMIN"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="В меню",
            callback_data="toStart"
        )
    )
    await message.answer(
        text="Выберите пункт меню",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "toMessage")
async def support_number(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.feedback_number)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toFeedback"
        )
    )
    await callback.message.answer(
        text="Введите ваш номер телефона:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.feedback_number)
async def support_message(message: Message, state: FSMContext):
    await state.set_state(Form.feedback_message)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toMessage"
        )
    )
    data.update(
        {
            message.from_user.id: {
                'number': message.text,
                'question': None
            }
        }
    )
    await message.answer(
        text="Напишите свой вопрос:",
        reply_markup=builder.as_markup()
    )


@router.message(Form.feedback_message)
async def support_message(message: Message, state: FSMContext):
    await state.clear()
    data[message.from_user.id]['question'] = message.text
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="toStart"
        )
    )
    admin_builder = InlineKeyboardBuilder()
    await message.answer(
        text="Ваше сообщение отправлено",
        reply_markup=builder.as_markup()
    )
    if message.from_user.username:
        username = f'@{message.from_user.username}'
    else:
        username = message.from_user.first_name
    cur = db.cursor()
    cur.execute("INSERT INTO tickets (user_id, username, number, text) VALUES (?,?,?,?)",
                (message.from_user.id, username, data[message.from_user.id]['number'], data[message.from_user.id]['question']))
    db.commit()
    num = cur.execute(
            f"SELECT ticket_id FROM tickets WHERE user_id == {message.from_user.id} ORDER BY ticket_id DESC").fetchone()[0]
    admin_builder.row(
        InlineKeyboardButton(
            text="Взять в работу",
            callback_data=f"admin_accept_feedback_{num}"
        )
    )
    await bot.send_message(
        chat_id=-4151447179,
        text=emoji.emojize(
            f"Поступила новая заявка от пользователя {username}\n"
            f"Номер заявки: {num}\n"
            f"Номер телефона: {data[message.from_user.id]['number']}\n"
            f"Текст сообщения: "
            f"{data[message.from_user.id]['question']}"
        ),
        reply_markup=admin_builder.as_markup()
    )
