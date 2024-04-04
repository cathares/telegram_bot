from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
)

import emoji

from states import Form
router = Router()


@router.message(Command("new_order"))
async def new_order_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.article)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        "Введите артикул:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(StateFilter(Form.size, Form.main_menu), F.data == "toArticle")
async def back_to_article_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.article)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        "Ввведите артикул:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.article)
async def sizeHandler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.size)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toArticle"
        )
    )
    await message.answer(
        "Ввведите размер:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.name, F.data == "toSize")
async def back_to_size_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.size)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toArticle"
        )
    )
    await callback.message.answer(
        "Ввведите размер:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.size)
async def name_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toSize"
        )
    )
    await message.answer(
        "Ввведите ФИО:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.number, F.data == "toName")
async def back_to_name_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.name)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toSize"
        )
    )
    await callback.message.answer(
        "Ввведите ФИО:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.name)
async def number_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.number)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toName"
        )
    )
    await message.answer(
        "Ввведите номер телефона:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.address, F.data == "toNumber")
async def back_to_number_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.number)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toName"
        )
    )
    await callback.message.answer(
        "Ввведите номер телефона:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.number)
async def address_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.address)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toNumber"
        )
    )
    await message.answer(
        "Ввведите адрес СДЕКа:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.code, F.data == "toAddress")
async def back_to_address_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.address)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toNumber"
        )
    )
    await callback.message.answer(
        "Ввведите адрес СДЕКа:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.address)
async def code_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.code)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Пропустить"),
            callback_data="toCheck"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toAddress"
        )
    )
    await message.answer(
        "Ввведите промокод:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.check, F.data == "toCode")
async def back_to_code_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.code)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("Пропустить"),
            callback_data="toCheck"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toAddress"
        )
    )
    await callback.message.answer(
        "Ввведите промокод:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.code)
async def check_form(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.check)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":check_mark_button:Подтвердить заказ"),
            callback_data="accept"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Отменить заказ"),
            callback_data="cancel"
        ),
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toCode"
        )
    )
    await message.answer(
        "Проверьте правильность введенных данных:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.code, F.data == "toCheck")
async def skip_to_check_form(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.check)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":check_mark_button:Подтвердить заказ"),
            callback_data="accept"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Отменить заказ"),
            callback_data="cancel"
        ),
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toCode"
        )
    )
    await callback.message.answer(
        "Проверьте правильность введенных данных:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(Form.check, F.data == "accept")
async def accept(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="В меню",
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        "Заказ подтвержден!",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(Form.check, F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="В меню",
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        "Заказ отменен.",
        reply_markup=builder.as_markup()
    )
    await callback.answer()