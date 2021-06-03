from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buy_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтверждаю', callback_data='starting_buy'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_buy')
        ]
    ]
)
