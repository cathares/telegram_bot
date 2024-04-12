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
            text="Вызвать саппорта",
            callback_data="callSupport"
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
            text="Вызвать саппорта",
            callback_data="callSupport"
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
    InlineKeyboardButton(
        text=emoji.emojize(":cross_mark:Назад"),
        callback_data="toFeedback"
    )
    await callback.message.answer(
        text="Введите ваш номер телефона:"
    )
    await callback.answer()


@router.message(Form.feedback_number)
async def support_message(message: Message, state: FSMContext):
    await state.set_state(Form.feedback_message)
    await message.answer(
        text="Напишите свой вопрос:"
    )


@router.message(Form.feedback_message)
async def support_message(message: Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Вернуться в меню",
            callback_data="toStart"
        )
    )
    await message.answer(
        text="Ваше сообщение отправлено",
        reply_markup=builder.as_markup()
    )
