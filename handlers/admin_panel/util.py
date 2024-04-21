from aiogram.filters import Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import admin_ids
from db.database import db


class AdminStates(StatesGroup):
    message = State()
    rate = State()
    markup = State()
    usual_delivery = State()
    fast_delivery = State()
    admin_promo = State()
    admin_promo_quant = State()
    change_promo_quant = State()


class AdminFilter(Filter):
    async def __call__(self, message: Message):
        cur = db.cursor()
        return message.from_user.id in admin_ids
