from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import allow_access


@allow_access()
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
	    "/promo - Ввести реферальный промокод(Могут только незарегестрированные пользователи!)")
    
    await message.answer("\n".join(text))
