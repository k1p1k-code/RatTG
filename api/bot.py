from core.loader import bot, dp
from type import TypeInfo

from aiogram import F
from aiogram.types import Update
from fastapi import APIRouter, Request
from pydantic import BaseModel

router_bot=APIRouter(prefix='/bot', tags=['bot_control'])

@router_bot.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
