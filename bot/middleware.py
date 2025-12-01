from aiogram import BaseMiddleware
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update, Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from core.loader import config

class UserBase(BaseMiddleware):
    async def __call__(
        self,
        handlers: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]) -> Any:
        if (event.message or event.callback_query or event.inline_query).from_user.id == config.admin_id_tg:
            return await handlers(event, data)