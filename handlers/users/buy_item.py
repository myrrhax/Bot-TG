from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton

from data import config
from data.Item import Item, REGULAR_POST_SHIPPING, FAST_POST_SHIPPING
from utils.db_api import db_commands as commands
from keyboards.inline.menu import buy_callback
from loader import dp, bot
from utils.misc.generate_price import generate_amount_price
from utils.misc.shipping_address import ShippingAddressAsDict


@dp.callback_query_handler(buy_callback.filter())
async def get_count(call: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data.get('item_id')
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer('Введите количество товара')
    async with state.proxy() as data:
        data['item_id'] = item_id
    await state.set_state('get_count')


@dp.message_handler(state='get_count')
async def get_count(message: Message, state: FSMContext):
    try:
        count = int(message.text)
        if count > 0:
            user_id = message.from_user.id
            current_score = await commands.check_score(user_id)
            async with state.proxy() as data:
                data['count'] = count
            if current_score > 0:
                await message.answer(f'У вас {current_score} баллов'
                                     f' (1 балл = 1$). Сколько баллов вы хотите использовать?')
                await state.set_state('set_ref_score')
            else:
                async with state.proxy() as data:
                    data['used_score'] = 0
                await invoice_to_buy(message, state)
        else:
            await message.answer('Количесво должно превышать 0')
    except ValueError:
        await message.answer('Пожалуйста, введите количество в виде числа.')


@dp.message_handler(state='set_ref_score')
async def get_score(message: Message, state: FSMContext):
    try:
        used_score = int(message.text)
        user_id = message.from_user.id
        current_score = await commands.check_score(user_id)
        if used_score > current_score:
            await message.answer('У вас нет столько реферальных баллов!')

        if current_score - used_score <= 0:
            await message.answer('Цена должна быть больше нуля!')

        async with state.proxy() as data:
            data['user_score'] = used_score
        await invoice_to_buy(message, state)
    except Exception:
        await message.answer('Введите количество баллов в виде числа!')


async def invoice_to_buy(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    count = data.get('count')
    used_score = data.get('used_score')
    item = await commands.select_item(item_id)
    price = int(item.price)
    amount = price * count - used_score
    amount = await generate_amount_price(amount)
    await state.reset_state(with_data=False)
    invoice_item = Item(
        title=item.name,
        description=item.description,
        currency="USD",
        prices=[
            LabeledPrice(
                label=item.name,
                amount=amount
            )
        ],
        start_parameter=f'create_invoice_{item_id}',
        photo_url=item.photo,
        photo_height=400,
        photo_width=400,
        need_shipping_address=True,
        is_flexible=True
    )

    await bot.send_invoice(
        message.from_user.id,
        **invoice_item.generate_invoice(),
        payload=item.item_id)


@dp.shipping_query_handler()
async def test(query: types.ShippingQuery, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = query.shipping_address
    await bot.answer_shipping_query(query.id,
                                    shipping_options=[REGULAR_POST_SHIPPING, FAST_POST_SHIPPING],
                                    ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    data = await state.get_data()
    address = data.get('address')
    used_score = data.get('used_score')
    item_id = data.get('item_id')
    count = data.get('count')

    city = address['city']
    region = address['state']
    post_code = address['post_code']
    street = address['street_line1']

    amount = pre_checkout_query.total_amount
    amount = str(amount)[0:len(str(amount))-2]

    item = await commands.select_item(item_id)
    shipping_address = ShippingAddressAsDict(
        city=city,
        region=region,
        street=street,
        post_address=post_code,
    ).generate_shipping_query()
    user = await commands.select_user(pre_checkout_query.from_user.id)
    await commands.minus_score(user_id=pre_checkout_query.from_user.id,
                               score=used_score)

    for admin in config.ADMINS:
        await bot.send_message(admin,
                               text=f'Пользователь {pre_checkout_query.from_user.get_mention(as_html=True)} '
                                    f'купил {item.name} в количесве {count} по цене: {amount}$\n'
                                    f'Адресс доставки:\n'
                                    f'Город: {city}\n'
                                    f'Область: {region}\n'
                                    f'Код почты: {post_code}\n'
                                    f'Улица: {street}')

    await commands.add_to_buy(user_id=user,
                              item_id=item,
                              price=int(amount),
                              quantity=count,
                              shipping_address=shipping_address
                              )

    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Спасибо за покупку! Ожидайте отправку")


