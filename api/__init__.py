from .info import router_info
from .media import router_media
from .bot import router_bot

def register(app):
    for i in [router_info, router_media, router_bot]:
        app.include_router(i)