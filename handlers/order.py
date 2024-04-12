from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
)
import emoji
from db.database import db
from main import bot
from states import Form

router = Router()

current_orders = {}


@router.message(Command("new_order"))
async def new_order_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.article)
    current_orders.update(
        {
            message.from_user.id: {
                'article': None,
                'size': None,
                'name': None,
                'number': None,
                'address': None,
                'code': None
            }
        }
    )
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize(":cross_mark:Назад"),
            callback_data="toStart"
        )
    )
    await message.answer(
        emoji.emojize("🛒Введите артикул:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(StateFilter(Form.size, Form.main_menu), F.data == "toArticle")
async def back_to_article_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.article)
    current_orders.update(
        {
            callback.from_user.id: {
                'article': None,
                'size': None,
                'name': None,
                'number': None,
                'address': None,
                'code': None
            }
        }
    )
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        emoji.emojize("🛒Введите артикул:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.article)
async def sizeHandler(message: Message, state: FSMContext) -> None:
    current_orders[message.from_user.id]['article'] = message.text
    await state.set_state(Form.size)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toArticle"
        )
    )
    await message.answer(
        emoji.emojize("📐Ввведите размер:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.name, F.data == "toSize")
async def back_to_size_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.size)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toArticle"
        )
    )
    await callback.message.answer(
        emoji.emojize("📐Ввведите размер:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.size)
async def name_handler(message: Message, state: FSMContext) -> None:
    current_orders[message.from_user.id]['size'] = message.text
    await state.set_state(Form.name)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toSize"
        )
    )
    await message.answer(
        emoji.emojize("🪪Ввведите ФИО:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.number, F.data == "toName")
async def back_to_name_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.name)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toSize"
        )
    )
    await callback.message.answer(
        emoji.emojize("🪪Ввведите ФИО:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.name)
async def number_handler(message: Message, state: FSMContext) -> None:
    current_orders[message.from_user.id]['name'] = message.text
    await state.set_state(Form.number)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toName"
        )
    )
    await message.answer(
        emoji.emojize("☎Ввведите номер телефона:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.address, F.data == "toNumber")
async def back_to_number_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.number)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toName"
        )
    )
    await callback.message.answer(
        emoji.emojize("☎Ввведите номер телефона:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.number)
async def address_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.address)
    current_orders[message.from_user.id]['number'] = message.text
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toNumber"
        )
    )
    await message.answer(
        emoji.emojize("🚛Ввведите адрес СДЕКа:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.code, F.data == "toAddress")
async def back_to_address_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.address)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toNumber"
        )
    )
    await callback.message.answer(
        emoji.emojize("🚛Ввведите адрес СДЕКа:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.address)
async def code_handler(message: Message, state: FSMContext) -> None:
    current_orders[message.from_user.id]['address'] = message.text
    await state.set_state(Form.code)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("➡Пропустить"),
            callback_data="toCheck"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toAddress"
        )
    )
    await message.answer(
        text=emoji.emojize("🏷Ввведите промокод:"),
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.check, F.data == "toCode")
async def back_to_code_callback(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.code)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("➡Пропустить"),
            callback_data="toCheck"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize("⬅Назад"),
            callback_data="toAddress"
        )
    )
    await callback.message.answer(
        text=emoji.emojize("🏷Ввведите промокод:"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.message(Form.code)
async def check_form(message: Message, state: FSMContext) -> None:
    current_orders[message.from_user.id]['code'] = message.text
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
            text=emoji.emojize("⬅Назад"),
            callback_data="toCode"
        )
    )
    await message.answer(
        emoji.emojize(f"<b>Проверьте правильность введенных данных:</b>"
                      f"\n🛒Артикул: {current_orders[message.from_user.id]['article']} "
                      f"\n📐Размер:"f" {current_orders[message.from_user.id]['size']}"
                      f"\n👥ФИО:"f" {current_orders[message.from_user.id]['name']}"
                      f"\n☎Номер телефона: {current_orders[message.from_user.id]['number']}"
                      f"\n🚛Адрес СДЕКа: {current_orders[message.from_user.id]['address']}"
                      f"\n🏷Промокод: {current_orders[message.from_user.id]['code']}"),
        parse_mode='HTML',
        reply_markup=builder.as_markup()
    )


@router.callback_query(Form.code, F.data == "toCheck")
async def skip_to_check_form(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Form.check)
    current_orders[callback.from_user.id]['code'] = ''
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
            text=emoji.emojize("⬅Назад"),
            callback_data="toCode"
        )
    )
    await callback.message.answer(
        emoji.emojize(f"<b>Проверьте правильность введенных данных</b>:"
                      f"\n🛒Артикул: {current_orders[callback.from_user.id]['article']} "
                      f"\n📐Размер:"f" {current_orders[callback.from_user.id]['size']}"
                      f"\n👥ФИО:"f" {current_orders[callback.from_user.id]['name']}"
                      f"\n☎Номер телефона: {current_orders[callback.from_user.id]['number']}"
                      f"\n🚛Адрес СДЕКа: {current_orders[callback.from_user.id]['address']}"
                      ),
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )

    await callback.answer()


@router.callback_query(Form.check, F.data == "accept")
async def accept(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    cur = db.cursor()
    cur.execute(f"INSERT INTO orders (user_id, username, article, size, name, phone_number, address, promocode, status)"
                f"VALUES (?,?,?,?,?,?,?,?,?)", (
                    callback.from_user.id,
                    f'@{callback.from_user.username}',
                    current_orders[callback.from_user.id]['article'],
                    current_orders[callback.from_user.id]['size'],
                    current_orders[callback.from_user.id]['name'],
                    current_orders[callback.from_user.id]['number'],
                    current_orders[callback.from_user.id]['address'],
                    current_orders[callback.from_user.id]['code'],
                    "accepted"
                )
                )
    db.commit()
    num = cur.execute(f"SELECT order_id FROM orders WHERE user_id == {callback.from_user.id} ORDER BY order_id DESC").fetchone()[0]
    cur.close()

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅В меню"),
            callback_data="toStart"
        )
    )
    admin_msg_builder = InlineKeyboardBuilder()
    admin_msg_builder.row(
        InlineKeyboardButton(
            text="Взять в работу",
            callback_data=f"admin_order_{num}"
        )
    )
    await bot.send_message(
        chat_id=-4168941250,
        text=emoji.emojize(f"<b>Поступил новый заказ:</b>"
                           f"\nНомер заказа: {num}\n"
                           f"Имя пользователя: @{callback.from_user.username}"
                           f"\n🛒Артикул: {current_orders[callback.from_user.id]['article']} "
                           f"\n📐Размер:"f" {current_orders[callback.from_user.id]['size']}"
                           f"\n👥ФИО:"f" {current_orders[callback.from_user.id]['name']}"
                           f"\n☎Номер телефона: {current_orders[callback.from_user.id]['number']}"
                           f"\n🚛Адрес СДЕКа: {current_orders[callback.from_user.id]['address']}" +
                           f"\n🏷Промокод: {current_orders[callback.from_user.id]['code']}"
                           ),
        reply_markup=admin_msg_builder.as_markup(),
        parse_mode='HTML'
    )
    await callback.message.answer(
        emoji.emojize(":check_mark_button:Заказ подтвержден!"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(Form.check, F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("⬅В меню"),
            callback_data="toStart"
        )
    )
    await callback.message.answer(
        text=emoji.emojize("Заказ отменен"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()
