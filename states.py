from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    article = State()
    size = State()
    number = State()
    address = State()
    code = State()
    check = State()
    main_menu = State()
    newOrder = State()
    orderList = State()
    calc = State()
    calc_delivery = State()
    calc_price = State()
    about = State()
    FAQ = State()
    partners = State()
    reviews = State()
    feedback = State()
    feedback_number = State()
    feedback_message = State()
