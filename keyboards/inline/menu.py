from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

menu_callback = CallbackData('menu', 'application')

menu_keyboard = InlineKeyboardMarkup(
    row_width=4,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Товары🛒',
                                 switch_inline_query_current_chat=''),
            InlineKeyboardButton(text='Реферальная система',
                                 callback_data=menu_callback.new(application='referral'))
        ],
        [
            InlineKeyboardButton(text='Админ панель',
                                 callback_data=menu_callback.new(application='admin_panel'))
        ],
        [InlineKeyboardButton(text='Отмена',
                              callback_data=menu_callback.new(application='cancel'))
         ]
    ]
)
