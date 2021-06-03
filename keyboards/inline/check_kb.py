from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

checkout_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Проверить платёж', callback_data='checkout'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_payment')
        ]
    ]
)
