from aiogram.dispatcher.filters.state import StatesGroup, State


class BuyState(StatesGroup):
    start_buy = State()
    set_count = State()
    set_score = State()
    set_pay_answer = State()
    check_qiwi = State()
    request_city = State()
    request_street = State()
    request_address_number = State()
    set_phone_number = State()
    set_comment_answer = State()
    set_comment = State()
