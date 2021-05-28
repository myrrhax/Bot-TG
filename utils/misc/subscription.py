from typing import Union

from aiogram import Bot


async def check_sub(user_id, channel: Union[int, str]):
    """Функция, проверяющая подписку"""
    bot = Bot.get_current()
    member = await bot.get_chat_member(chat_id=channel,
                                       user_id=user_id)
    return member.is_chat_member()
