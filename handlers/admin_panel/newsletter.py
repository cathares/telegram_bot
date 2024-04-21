from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.database import db
from handlers.admin_panel.util import AdminFilter, AdminStates

router = Router()


@router.callback_query(AdminFilter(), F.data == "ToNewsletter")
async def newsletter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.message)
    await callback.message.answer("Отправьте сообщение для рассылки")
    await callback.answer()


@router.message(AdminFilter(), AdminStates.message)
async def send_newsletter(message: Message, state: FSMContext):
    await message.answer("Подождите, идет отправка...")
    cur = db.cursor()
    users = cur.execute("SELECT user_id from users").fetchall()
    for user in users:
        try:
            await message.send_copy(chat_id=user[0])
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()
