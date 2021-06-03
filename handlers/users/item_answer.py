import re
import logging

from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

from handlers.users.start import bot_answer_user
from keyboards.inline import menu_callback
from loader import dp, bot
from utils.db_api import db_commands as commands


@dp.inline_handler()
async def show_items(query: types.InlineQuery):
    """Все товары"""
    name = query.query
    logging.info(name)
    # Если ничего нет то выдаем все товары
    if name == '':
        catalog = await commands.select_all_items()
    # Если юзер что-то написал, пробуем найти этот товар
    else:
        catalog = await commands.inline_selector(name.lower())
        # Если товар не найден
        if not catalog:
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        id='unknown_item',
                        title=f'Прости, я не могу найти товар {name}.',
                        input_message_content=InputTextMessageContent(
                            message_text='Товар не найден!'
                        )
                    )
                ]
            )
    # Формируем ответ
    answer_catalog = []
    for item in catalog:
        link = await get_start_link(payload=item.item_id)
        answer = InlineQueryResultArticle(
            id=f'{item.item_id}',
            title=f'{item.name}',
            description=f'{item.description}\n'
                        f'Цена: {item.price}$',
            thumb_url=f'{item.thumb}',
            input_message_content=InputTextMessageContent(
                message_text=f'Информация о товаре {item.name}\n'
                             f'Цена: {item.price}$\n'
                             f'Описание: {item.description}\n'
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='О товаре', url=link)
                    ]
                ]
            )
        )
        answer_catalog.append(answer)
    # Отвечаем
    await query.answer(
        results=answer_catalog
    )


