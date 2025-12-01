from core.loader import dp
from utils.get_info import check_on
from bot.keyb import menu

from aiogram import types, F
import asyncio

@dp.message(F.text == '/start')
async def cmd_start(message: types.Message):
    asyncio.create_task(check_on(cmd_start_prediction, ({'message':message})))

async def cmd_start_prediction(on_pc, message: types.Message):
    """Колбэк для обновления меню после сбора информации"""

    if on_pc:
        updated_markup = await menu.main_menu(on_pc)
        await message.answer('Choose a PC for interactions(only work)', 
                               reply_markup=updated_markup)
    else:
        await message.answer('No PCs available', 
                               reply_markup=await menu.main_menu(on_pc))