from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import menu_callback

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить товар', callback_data=menu_callback.new(application='add_item')),
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data=menu_callback.new(application='cancel_panel'))
        ]
    ]
)


confirmation_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтверждаю', callback_data=menu_callback.new(application='confirm')),
            InlineKeyboardButton(text='Отмена', callback_data=menu_callback.new(application='cancel_add'))
        ]
    ]
)

