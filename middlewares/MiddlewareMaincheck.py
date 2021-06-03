from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from data import config
from utils.db_api import db_commands as commands
from utils.misc import subscription


class MainChecker(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        #  Берём ID
        if update.message:
            user_id = update.message.from_user.id
            name = update.message.from_user.full_name
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
            name = update.callback_query.from_user.full_name
        else:
            return
        #  Чекаем юзера в БД
        user = await commands.select_user(user_id)
        #  Если есть, то просто продолжаем
        if user:
            return
        #  Если юзера нет, то проверяем есть ли он в канале
        else:
            channel = config.CHANNEL
            status = await subscription.check_sub(user_id, channel=channel)
            #  Если есть добавляем
            if status:
                await commands.add_user(user_id=user_id, name=name)
                await update.message.answer('Спасибо за подписку, теперь вы можете пользоваться ботом!')
            #  Если нет продолжаем обработку
            else:
                return
