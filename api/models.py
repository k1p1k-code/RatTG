from pydantic import BaseModel
from type import TypeInfo

class InfoPcForm(BaseModel):
    uuid: str
    name_short: str
    machine: str
    processor: str
    user: str

class RequestPollingForm(BaseModel):
    typePolling: TypeInfo.literal # pyright: ignore[reportInvalidTypeForm]
    zombie: str
