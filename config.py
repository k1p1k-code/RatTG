from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class SettingsRat(BaseSettings):
    host: HttpUrl
    token_bot_tg: str
    admin_id_tg: int