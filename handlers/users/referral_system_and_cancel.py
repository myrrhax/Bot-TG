from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from keyboards.inline import menu_callback
from loader import dp


# Ответ на кнопку Реферальная система
@dp.callback_query_handler(menu_callback.filter(application='referral'))
async def referral_system(call: types.CallbackQuery):
    await call.answer()
    referrer_id = call.from_user.id
    referral_link = await get_start_link(payload=referrer_id)
    await call.message.answer(f'Привет {call.from_user.get_mention(as_html=True)}! '
                              f'Вот твоя <b>реферальная ссылка</b>: {referral_link}\n'
                              f'Твой промокод: {referrer_id}')


# Ответ на кнопку отмена
@dp.callback_query_handler(menu_callback.filter(application='cancel'))
async def cancel_menu(call: types.CallbackQuery):
    await call.answer('Вы отменили действие', show_alert=False)
    await call.message.delete()
