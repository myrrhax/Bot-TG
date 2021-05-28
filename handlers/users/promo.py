import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from utils.db_api import db_commands as commands
from utils.misc import allow_access


@allow_access()
@dp.message_handler(Command('promo'))
async def bot_echo(message: types.Message, state: FSMContext):
    """По этой комнаде незарегестрированный пользователь сможет ввести промокод, для входа"""
    user_id = message.from_user.id
    user = await commands.select_user(user_id)
    #  Если он незарегестрированный
    if not user:
        await message.answer(f'Привет {message.from_user.get_mention(as_html=True)}!\n'
                             f'Введи промокод.')
        await state.set_state('promo')
    #  Если он уже был в базе
    else:
        await message.answer('Вы уже есть в базе!')


@allow_access()
@dp.message_handler(state='promo')
async def set_promo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    try:
        #  Если промокод - цифры
        referrer_id = int(text)
        referrer = await commands.select_user(referrer_id)
        # Если такого реферера нет
        if not referrer:
            await message.answer('Неверный код приглашения')
            return
        # Если реферер есть
        else:
            await commands.add_user(user_id=user_id,
                                    name=message.from_user.full_name)
            await commands.add_referral(referral=user_id,
                                        referrer=referrer_id)
            await commands.update_score(referrer_id)
            await message.answer('Спасибо, теперь вы можете пользоваться ботом!')
            await bot.send_message(chat_id=referrer_id,
                                   text='Пользователи ввёл ваш код приглашения, вам начислено 10 баллов')
    # Ошибка в промокоде
    except ValueError:
        await message.answer('Неверный код приглашения')

    await state.finish()

