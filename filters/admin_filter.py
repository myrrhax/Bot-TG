from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class IsAdmin(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        user = str(call.from_user.id)
        return user in config.ADMINS
