from core.TasksMenager import TasksMenager
from config import SettingsRat

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise, tortoise_exception_handlers
from collections.abc import AsyncGenerator
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
config=SettingsRat()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    url_webhook=str(config.host)+'bot/webhook'
    await bot.set_webhook(url=url_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    

    db_path=Path('database') / 'db.sqlite3'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Правильная конфигурация Tortoise
    config_tortoise={
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {
                    "file_path": str(db_path.resolve()),  # Абсолютный путь
                },
            },
        },
        "apps": {
            "models": {
                "models": ["database.models"],  # Убедитесь что models существует
                "default_connection": "default",
            },
        },
        "use_tz": False,
        "timezone": "UTC",
    }
    
    try:
        async with RegisterTortoise(
            app=app,
            config=config_tortoise,
            generate_schemas=True,  # Автоматическое создание таблиц
            add_exception_handlers=True,
        ):
            # База данных подключена
            yield
            # Завершение работы приложения
            
    finally:
        # Всегда закрываем соединения
        await Tortoise.close_connections()
        await bot.delete_webhook()

tasks=TasksMenager()
bot=Bot(token=config.token_bot_tg)
dp=Dispatcher()
app=FastAPI(lifespan=lifespan)