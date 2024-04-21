from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton, CallbackQuery,
)
import emoji

from handlers.admin_panel.util import AdminFilter
from start_bot import bot
from config import TICKETS_STATUS_LIST
from db.database import db
router = Router()


@router.callback_query(AdminFilter(), F.data.startswith("admin_accept_feedback_"))
async def accept_feedback(callback: CallbackQuery):
    num = callback.data[22:]
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=emoji.emojize("🕐Заявка в работе"),
            callback_data="NULL"
        )
    )
    cur = db.cursor()
    if cur.execute("SELECT worker FROM tickets WHERE ticket_id=={id}".format(id=num)).fetchone()[0] is None:
        cur.execute(
            "UPDATE tickets SET worker={worker}, message_id={message_id}, status='accepted' WHERE ticket_id=={id}".format(
                worker=callback.from_user.id,
                message_id=callback.message.message_id,
                id=num
            )
        )
        db.commit()
        await callback.message.reply(f"Заявка №{num} взята пользователем {callback.from_user.first_name}")
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )
    else:
        pass
    await callback.answer()


@router.callback_query(AdminFilter(), F.data == "admin_toTickets")
async def ticketsInWork(callback: CallbackQuery):
    cur = db.cursor()
    tickets = cur.execute("SELECT * FROM tickets WHERE worker == {worker} AND status != 'closed' ".format(
        worker=callback.from_user.id)).fetchall()
    if tickets:
        for i in range(0, len(tickets)):
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(
                    text="Закрыть заявку",
                    callback_data=f"CloseTicket{tickets[i][0]}"
                )
            )
            await callback.message.answer(
                text=emoji.emojize(
                    f"\nНомер заявки: {tickets[i][0]}\n"
                    f"Имя пользователя: {tickets[i][2]}"
                    f"\nНомер: {tickets[i][3]} "
                    f"\nСообщение: {tickets[i][4]}"
                    f"\nСтатус: {TICKETS_STATUS_LIST[tickets[i][6]]}"
                ),
                reply_markup=builder.as_markup()
            )
    else:
        await callback.message.answer(text="Заявок пока нет")
    await callback.answer()


@router.callback_query(AdminFilter(), F.data.startswith("CloseTicket"))
async def closeTicket(callback: CallbackQuery):
    ticket_id = callback.data[11:]
    cur = db.cursor()
    cur.execute("UPDATE tickets SET status = 'closed' WHERE ticket_id == {id}".format(id=ticket_id))
    db.commit()
    messageID = cur.execute("SELECT message_id FROM tickets WHERE ticket_id == {id}".format(id=ticket_id)).fetchone()[0]
    cur.close()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=emoji.emojize(":check_mark_button:Заявка закрыта"),
            callback_data="NULL"
        )
    )
    await bot.edit_message_reply_markup(
        chat_id=-4151447179,
        message_id=int(messageID),
        reply_markup=builder.as_markup()
    )
    await callback.message.answer(text=f"Заявка №{ticket_id} закрыта")
    await callback.message.delete()
    await callback.answer()