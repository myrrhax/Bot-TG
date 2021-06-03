from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from filters import IsAdmin
from handlers.users.start import bot_answer_user
from keyboards.inline import menu_callback
from keyboards.inline.admin_panel import admin_kb, confirmation_kb
from loader import dp
from utils.db_api import db_commands as commands


#  Админ пытается зайти
@dp.callback_query_handler(menu_callback.filter(application='admin_panel'), IsAdmin())
async def admin_panel(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Выберите действие',
                                 reply_markup=admin_kb)


#  Заходит не админ
@dp.callback_query_handler(menu_callback.filter(application='admin_panel'))
async def admin_panel(call: types.CallbackQuery):
    await call.answer('Вы не администратор', show_alert=False)


# Добавить товар
@dp.callback_query_handler(menu_callback.filter(application='add_item'))
async def enter_name(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer('Введите название товара: ')
    await state.set_state('name')


# Отмена
@dp.callback_query_handler(menu_callback.filter(application='cancel_panel'))
async def cancel_admin_panel(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    await bot_answer_user(call.message)


# Вводится имя
@dp.message_handler(state='name')
async def enter_(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data['name'] = name
    await message.answer('Введите ссылку на фото размера thumb'
                         '(Фото отображаемое в инлайн моде)')
    await state.set_state('thumb')


# Фото превью в инлайн моде
@dp.message_handler(state='thumb')
async def enter_(message: types.Message, state: FSMContext):
    thumb = message.text
    async with state.proxy() as data:
        data['thumb'] = thumb
    await message.answer('Пришлите фото товара')
    await state.set_state('photo')


# Фото
@dp.message_handler(state='photo', content_types=types.ContentType.PHOTO)
async def enter_(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    async with state.proxy() as data:
        data['photo'] = photo
    await message.answer('Введите описание товара')
    await state.set_state('description')


# Описание
@dp.message_handler(state='description')
async def enter_(message: types.Message, state: FSMContext):
    description = message.text
    async with state.proxy() as data:
        data['description'] = description
    await message.answer('Введите цену товара')
    await state.set_state('price')


# Цена и скидывается введенная инфа о товаре
@dp.message_handler(state='price')
async def enter_(message: types.Message, state: FSMContext):
    price = message.text

    async with state.proxy() as data:
        data['price'] = price

    data = await state.get_data()
    name = data.get('name')
    thumb = data.get('thumb')
    photo = data.get('photo')
    description = data.get('description')

    await message.answer_photo(photo=photo, caption='Фото товара')
    await message.answer('Вы хотите добавить товар:\n'
                         f'Имя: {name}\n'
                         f'Ссылка на фото thumb: {thumb}\n'
                         f'Описание: {description}\n'
                         f'Цена: {price}',
                         disable_web_page_preview=True,
                         reply_markup=confirmation_kb)
    await state.set_state('decision')


# Админ согласить добавить товар
@dp.callback_query_handler(menu_callback.filter(application='confirm'), state='decision')
async def confirm_add(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    data = await state.get_data()
    name = data.get('name')
    thumb = data.get('thumb')
    photo = data.get('photo')
    description = data.get('description')
    price = data.get('price')
    await state.finish()
    await commands.add_item(name, thumb, photo, description, price)
    await call.message.answer('Товар был успешно добавлен!')


# Админ не согласен добавлять товар
@dp.callback_query_handler(menu_callback.filter(application='cancel_add'), state='decision')
async def cancel_add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.answer('Вы отменили добавление товара')
