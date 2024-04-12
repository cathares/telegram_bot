import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def back_button(toState):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=emoji.emojize("⬅Назад"), callback_data=f'{toState}')],
    ])
