import os

from aiogram.fsm.storage.memory import MemoryStorage


admin_ids = {668979795, 536249650, 5485114818, 5923651217}
STATUS_LIST = {
    'accepted': 'В обработке',
    'delievering': 'В пути',
    'delievered': 'Доставлен'
}
TICKETS_STATUS_LIST = {
    'accepted': 'В обработке',
    'closed': 'Обработано'
}

my_orders_text_template = "<b>Номер заказа: {order_num}</b>" \
                          "\n🛒Артикул: {article} " \
                          "\n📐Размер: {size}" \
                          "\n👥ФИО: {name}" \
                          "\n☎Номер телефона: {phone_number}" \
                          "\n🚛Адрес СДЕКа: {address}" \
                          "\n🏷Промокод: {promo if promo is not None else ''}" \
                          "\n🕐Статус заказа: {status}\n"
