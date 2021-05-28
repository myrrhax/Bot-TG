import os

import django
from utils.notify_admins import on_startup_notify

from django_project.telegrambot.telegrambot import settings



async def on_startup(dp):
    import middlewares, filters, handlers
    from utils.set_bot_commands import set_default_commands
    await on_startup_notify(dp)
    await set_default_commands(dp)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "django_project.telegrambot.telegrambot.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
