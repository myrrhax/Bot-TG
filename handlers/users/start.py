import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.menu import buy_callback, menu_kb
from loader import dp, bot
from utils.misc import allow_access

from utils.db_api import db_commands as commands


# Ловим товары
@dp.message_handler(CommandStart(deep_link=re.compile(r'^[0-9]{1,5}$')))
async def selected_item(message: types.Message, state: FSMContext):
    item_arg = int(message.get_args())
    item = await commands.select_item(item_arg)
    if not item:
        await message.answer('Такого товара не существует')
    else:
        await message.answer_photo(
            photo=item.photo,
            caption=f'Подробнее о товаре {item.name}:\n'
                    f'Цена: {item.price}$.\n'
                    f'Описание: {item.description}',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Купить',
                                             callback_data=buy_callback.new(
                                                 item_id=item.item_id
                                             )),
                        InlineKeyboardButton(text='Отмена',
                                             callback_data='cancel')
                    ]
                ]
            )
        )


# Ловим старт по рефералке
@allow_access()
@dp.message_handler(CommandStart(deep_link=re.compile(r'^[0-9]{5,15}$')))
async def bot_start(message: types.Message):
    """Старт с диплинком"""
    user_id = message.from_user.id
    name = message.from_user.full_name
    user = await commands.select_user(user_id)
    #  Если пользователя нет, то проверим диплинк
    if not user:
        #  Правильный диплинк
        try:
            referrer_id = int(message.get_args())
        except ValueError as err:
            await message.answer('Неправильная реферальная ссылка')
            return
        #  Проверяем существует реферер с таким id
        referrer = await commands.select_user(user_id=referrer_id)
        #  Если нет выдаём ошибку
        if not referrer:
            await message.answer('Неверная рефферальная ссылка')
            #  Если есть добавляем
        else:
            await commands.add_user(user_id, name)
            await commands.add_referral(referrer=referrer_id, referral=user_id)
            await commands.update_score(referrer_id)
            await message.answer('Спасибо, теперь вы можете пользоваеться ботом!')
            await bot.send_message(chat_id=referrer_id,
                                   text='Пользователь прешёл по вашей реферальной ссылке!\n'
                                        'Вам было начислено 10 баллов!')
    # Пользователь уже был в базе
    else:
        await message.answer(f'Привет, {message.from_user.get_mention(as_html=True)}!\n'
                             'Ты уже есть в базе данных!')


# Старт для пользователя
@dp.message_handler(CommandStart())
async def bot_answer_user(message: types.Message):
    """/start для, зарегистрированных пользователей"""
    keyboard = await menu_kb(message.from_user.id)
    await message.answer(f'Привет, {message.from_user.get_mention(as_html=True)}!\n'
                         f'Выбери действие!',
                         reply_markup=keyboard)
