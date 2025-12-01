from aiogram import Dispatcher

from .middleware import UserBase

from .handlers.menu import dp
from .handlers.control import dp

def register(dp: Dispatcher):
    for middleware in [UserBase]:
        dp.update.register(middleware)