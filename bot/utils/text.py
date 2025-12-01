from pydantic import BaseModel
from api.models import InfoPcForm

async def control_text(data: InfoPcForm | dict):
    if isinstance(data, InfoPcForm):
        data: InfoPcForm
        data=data.model_dump()
    return (f'User: {data["user"]}\n'
            f'UUID: {data["uuid"]}\n'
            f'Name short: {data["name_short"]}\n'
            f'Machine: {data["machine"]}\n'
            f'Processor: {data["processor"]}\n')