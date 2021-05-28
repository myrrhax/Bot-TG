from aiogram import Dispatcher

from loader import dp
from .MiddlewareMaincheck import MainChecker
from .throttling import ThrottlingMiddleware
from .locker import LockMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(MainChecker())
    dp.middleware.setup(LockMiddleware())
