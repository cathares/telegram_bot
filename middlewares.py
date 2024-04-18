from abc import ABC
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject, Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from start_bot import bot

'''
            async def on_process_message(self,
                                         message: Message,
                                         data: dict):
                user_channel_status = await bot.get_chat_member(chat_id='-1002086022026', user_id=message.from_user.id)
                if user_channel_status["status"] != 'left':
                    pass
                else:
                    await bot.send_message(message.from_user.id, 'Для доступа к боту необходимо быть подписанным '
                                                                 'на информационный канал: https://t.me/CHINA_TOWN_INFO')
                                                                 '''


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_channel_status = await bot.get_chat_member(chat_id=-1002086022026, user_id=event.from_user.id)
        if user_channel_status.status != 'left':
            result = await handler(event, data)
            return result
        else:
            builder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text="Проверить подписку",
                    callback_data= "toStart"
                )
            )
            if event is CallbackQuery:
                await event.answer()
            await bot.send_message(event.from_user.id, 'Для доступа к боту необходимо быть подписанным '
                                                       'на информационный канал: https://t.me/CHINA_TOWN_INFO',
                                   reply_markup=builder.as_markup()
                                   )
