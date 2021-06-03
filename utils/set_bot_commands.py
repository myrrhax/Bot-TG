from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('/start', 'Открыть меню'),
            types.BotCommand('/help', 'Информация о боте'),
            types.BotCommand('/promo', 'Ввести рефферальный промокод')
        ]
    )
