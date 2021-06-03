import re

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api import db_commands as commands


class LockMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        """Обрабатываем апдейты и проверяем, открыт хэндлер для незарегистрированных пользователей"""
        user_id = message.from_user.id
        user = await commands.select_user(user_id)
        # Юзер есть в БД
        if user:
            return
        # Юзера нет в БД
        else:
            handler = current_handler.get()
            if not handler:
                return
            #  Забираем атрибут с хэндлера
            allow = getattr(handler, 'allow', False)
            #  Хэндлер открытый
            if allow:
                return
            #  Хэндлер закрытый
            await message.answer('Чтобы использовать этого бота введите код приглашения,'
                                 'либо пройдите по реферальной ссылке!\n'
                                 'Также вы можете вступить в мой канал и получить доступ!'
                                 f'<a href="https://t.me/joinchat/QgwGeTcgQFo0YTIy">Вступить</a>')
            raise CancelHandler()
