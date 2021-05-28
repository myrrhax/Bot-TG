from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.markdown import hlink, hcode

from data import config
from data.config import ADMINS
from keyboards.inline.buy_kb import buy_buttons
from keyboards.inline.check_kb import checkout_kb
from loader import dp, bot
from states.buy_state import BuyState
from utils.db_api import db_commands as commands
from utils.misc import ShippingAddress
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


# Предлагаем выбрать количество товара
@dp.callback_query_handler(text='buy_item', state=BuyState.start_buy)
async def set_count_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer()
    await call.message.answer('Пожалуйста введите количество товара')
    await BuyState.set_count.set()


# Если пользователь отвечает сообщением
@dp.message_handler(state=BuyState.start_buy)
async def block_message(message: types.Message):
    await message.reply('Пожалуйтса выберите действие!')


# Отменил покупку
@dp.callback_query_handler(text='cancel_buy', state=BuyState.start_buy)
async def cancel_check(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.answer()
    await state.finish()


# Забираем количество и предлагаем выбрать количество баллов
@dp.message_handler(state=BuyState.set_count)
async def set_score_handler(message: types.Message, state: FSMContext):
    count = message.text
    user_id = message.from_user.id
    score = await commands.check_score(user_id)
    async with state.proxy() as data:
        data['score'] = score
        data['count'] = count
    #  Если баллы есть
    if score > 0:
        await message.answer(f'У вас {score} реферальных баллов (10 балл = 10 USD).\n'
                             f'Сколько баллов вы хотите использовать?')
        await BuyState.set_score.set()
    # Если баллов нет
    else:
        used_score = 0
        async with state.proxy() as data:
            data['used_score'] = used_score
        await message.answer('Подтвердите:\n'
                             f'Количество товара -> {count}',
                             reply_markup=buy_buttons)
        await BuyState.set_pay_answer.set()


# Забираем количество товара и подтверждаем количество и скидку
@dp.message_handler(state=BuyState.set_score)
async def get_score(message: types.Message, state: FSMContext):
    # Введенно верно
    try:
        used_score = int(message.text)
        data = await state.get_data()
        score = data.get('score')
        # Если пользователь ввёл больше баллов, чем у него есть
        if used_score > score:
            await message.reply('У вас нет столько баллов, пожалуйста введите количество меньшее'
                                ' или равное количеству ваших баллов')
        # Если все нормально
        else:
            count = data.get('count')
            item_id = data.get('item_id')
            item = await commands.select_item(item_id)
            # Если цена будет больше 0 со скидкой, то продолжаем
            if int(item.price) * int(count) - int(used_score) > 0:
                async with state.proxy() as data:
                    data['used_score'] = used_score
                await message.reply('Подтвердите:\n'
                                    f'Количество товара -> {count}\n'
                                    f'Количество баллов -> {used_score}', reply_markup=buy_buttons)
                await BuyState.set_pay_answer.set()
            # Иначе сообщим об этом
            else:
                await message.reply('Простите, но стоимость товара должна привышать 0!')
    # Введенно неверно
    except ValueError:
        await message.reply('Введите количество баллов в виде целого числа.')


# Пользователь отмненил покупку
@dp.callback_query_handler(text='cancel_buy', state=BuyState.set_pay_answer)
async def cancel_buy(call: types.CallbackQuery, state: FSMContext):
    await cancel_check(call, state)


# Пользователь согласен на покупку
@dp.callback_query_handler(text='starting_buy', state=BuyState.set_pay_answer)
async def buy_item(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item_id = data.get('item_id')
    used_score = data.get('used_score')
    count = data.get('count')
    item = await commands.select_item(item_id)
    price = int(item.price)
    total_price = price * int(count) - int(used_score)
    payment = Payment(amount=total_price)
    payment.create()
    async with state.proxy() as data:
        data['amount'] = total_price
        data['payment'] = payment
    await call.message.answer(
        "\n".join([
            f"Оплатите не менее {total_price:.2f}₽ по номеру телефона или по адресу: ",
            "",
            hlink(config.WALLET_QIWI, url=payment.invoice),
            "И обязательно укажите в качестве комментария ID платежа:",
            hcode(payment.id)
        ]), reply_markup=checkout_kb)
    await BuyState.check_qiwi.set()


# Отмена покупки
@dp.callback_query_handler(text='cancel_payment', state=BuyState.check_qiwi)
async def cancel_qiwi(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Вы отменили операцию!')
    await state.finish()


# Проверка операции
@dp.callback_query_handler(text='checkout', state=BuyState.check_qiwi)
async def check_qiwi_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get('payment')
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.answer()
        await call.message.answer('Перевод не найден!')
        return
    except NotEnoughMoney:
        await call.answer()
        await call.message.answer('Оплаченная сумма меньше необходимой!')
        return
    else:
        await call.message.answer("<i>Оплата прошла успешно! Уточните свой адресс для отправки.</i>"
                                  "\nВведите город.")
        await BuyState.request_city.set()

    await call.message.edit_reply_markup()


#  @dp.callback_query_handler(text='checkout', state=BuyState.check_qiwi)
#  async def test(call: types.CallbackQuery, state: FSMContext):
#    await call.message.answer("<i>Оплата прошла успешно! Уточните свой адресс для отправки.</i>"
#                              "\nВведите город.")
#    await BuyState.request_city.set()


# Ввод города
@dp.message_handler(state=BuyState.request_city)
async def get_city(message: types.Message, state: FSMContext):
    city = message.text
    async with state.proxy() as data:
        data['city'] = city
    await message.answer('Хорошо, теперь введите свою улицу')
    await BuyState.request_street.set()


# Ввод улицы
@dp.message_handler(state=BuyState.request_street)
async def get_street(message: types.Message, state: FSMContext):
    street = message.text
    async with state.proxy() as data:
        data['street'] = street

    await message.answer('Теперь введите свой номер дома.')
    await BuyState.request_address_number.set()


# Ввод номера дома
@dp.message_handler(state=BuyState.request_address_number)
async def get_house_number(message: types.Message, state: FSMContext):
    try:
        # Если номер введен числом
        house_number = int(message.text)
        async with state.proxy() as data:
            data['house_number'] = house_number

        await message.answer('Пожалуйста оставьте свой номер, чтобы мы могли связаться с вами!',
                             reply_markup=ReplyKeyboardMarkup(
                                 keyboard=[
                                     [
                                         KeyboardButton(text='Оставить номер',
                                                        request_contact=True)
                                     ]
                                 ], resize_keyboard=True
                             ))
        await BuyState.set_phone_number.set()
    except ValueError:
        # При ошибке
        await message.answer('Пожалуйста введите номер дома в виде числа!')


# Забираем номер телефона
@dp.message_handler(state=BuyState.set_phone_number, content_types=types.ContentType.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    async with state.proxy() as data:
        data['phone_number'] = phone_number
    await message.answer('Спасибо, осталось совсем немного!\n'
                         'Оставьте комментарий для покупки.'
                         ,reply_markup=ReplyKeyboardRemove())
    await BuyState.set_comment.set()


# Забираем комментарий для платежа и добавляем в БД с покупками, уведомляем админа
@dp.message_handler(state=BuyState.set_comment)
async def set_comment(message: types.Message, state: FSMContext):
    comment = message.text
    await message.answer('Спасибо за покупку!')
    data = await state.get_data()
    item_id = data.get('item_id')
    used_score = data.get('used_score')
    count = data.get('count')
    amount = data.get('amount')
    number = data.get('phone_number')
    city = data.get('city')
    street = data.get('street')
    house_number = data.get('house_number')
    if not comment:
        comment = 'Без коментария'
    info = ShippingAddress(city, street, house_number, comment)
    info = info.generate_shipping_query()
    user = await commands.select_user(message.from_user.id)
    item = await commands.select_item(item_id)
    buy_time = datetime.now()
    for admin in ADMINS:
        await bot.send_message(chat_id=admin,
                               text=f'Пользователь {message.from_user.get_mention(as_html=True)} совершил покупку!\n'
                                    f'Информация о покупке:\n'
                                    f'Время покупки: {buy_time}\n'
                                    f'ID товара: {item_id}\n'
                                    f'Потраченных реферальных очков: {used_score}\n'
                                    f'Количество товара: {count}\n'
                                    f'Сумма покупки: {amount}\n'
                                    f'Номер телефона: {number}')
    await commands.minus_score(user_id=int(message.from_user.id),
                               score=int(used_score))
    await commands.add_to_buy(user_id=user,
                              item_id=item,
                              price=amount,
                              quantity=count,
                              shipping_address=info,
                              phone_number=number)
    await state.finish()
