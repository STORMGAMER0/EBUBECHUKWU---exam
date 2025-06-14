from typing import Optional

from pydantic import BaseModel


class CreateEvent(BaseModel):
    title : str
    location : str
    date : str


class ResponseEvent(CreateEvent):
    event_id: int
    is_open: bool = True

class UpdateEvent(BaseModel):
    title : Optional[str] = None
    location : Optional[str] = None
    date : Optional[str] = None



