from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import config

menu_callback = CallbackData('menu', 'application')
buy_callback = CallbackData('buy', 'item_id')


async def menu_kb(user_id):
    menu_keyboard = InlineKeyboardMarkup(
        row_width=4,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Товары🛒',
                                     switch_inline_query_current_chat=''),
                InlineKeyboardButton(text='Реферальная система',
                                     callback_data=menu_callback.new(application='referral'))
            ]
        ]
    )

    if str(user_id) in config.ADMINS:
        menu_keyboard.row(
            InlineKeyboardButton(text='Админ-Панель',
                                 callback_data=menu_callback.new(application='admin_panel'))
        )

    menu_keyboard.row(
        InlineKeyboardButton(text='Отмена',
                             callback_data=menu_callback.new(application='cancel'))
    )

    return menu_keyboard
