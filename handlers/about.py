import emoji
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import Form

router = Router()


@router.message(Command("about"))
async def about_command_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.about)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("FAQ"),
            callback_data="toFAQ"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("Партнеры"),
            callback_data="toPartners"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Отзывы"),
            callback_data="toReviews"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        text="Выберите пункт меню",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "toAbout")
async def about_command_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.about)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("FAQ"),
            callback_data="toFAQ"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("Партнеры"),
            callback_data="toPartners"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Отзывы"),
            callback_data="toReviews"
        ),
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        text="Выберите пункт меню",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == "toFAQ")
async def FAQ_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.FAQ)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toAbout"
        )
    )
    await callback.message.answer(
        "FAQ:",
        reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "toPartners")
async def partners_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.partners)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toAbout"
        )
    )
    await callback.message.answer(
        "Партнеры:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == "toReviews")
async def partners_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.reviews)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toAbout"
        )
    )
    await callback.message.answer(
        "Отзывы:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()
