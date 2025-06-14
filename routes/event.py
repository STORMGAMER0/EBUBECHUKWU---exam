from typing import Dict

from fastapi import APIRouter,status

from database import Event
from schemas.event import ResponseEvent, CreateEvent, UpdateEvent
from services.event import EventService

event_router = APIRouter()

@event_router.post("/events", status_code=status.HTTP_201_CREATED, response_model=ResponseEvent)
def add_event(new_event : CreateEvent):
    event = EventService.create_event(new_event)
    return event

@event_router.get("/events", status_code=status.HTTP_200_OK,response_model=Dict[int, ResponseEvent])
def get_events():
    return Event

@event_router.get("/events/id/{event_id}", status_code=status.HTTP_200_OK,response_model=ResponseEvent)
def get_event_by_id(event_id : int):
    event = EventService.get_event(event_id)
    return event

@event_router.get("/events/title/{title}", status_code=status.HTTP_200_OK,response_model=ResponseEvent)
def get_event_by_title(title:str):
    event = EventService.get_event_title(title)
    return event

@event_router.put("/events/update/{event_id}", status_code=status.HTTP_200_OK,response_model=ResponseEvent)
def update_event(event_id : int, update: UpdateEvent):
    update = EventService.update_event(event_id,update)
    return update

@event_router.delete("/events/delete/{event_id}",status_code=status.HTTP_200_OK)
def delete_event(event_id:int):
    EventService.delete_event(event_id)
    return {"detail" : "event deleted successfully"}

@event_router.put("/events/close/{event_id}", status_code=status.HTTP_200_OK)
def close_event(event_id:int):
    EventService.close_event(event_id)
    return {"detail" : "event closed successfully"}


@event_router.put("/events/open/{event_id}", status_code=status.HTTP_200_OK)
def open_event(event_id:int):
    EventService.open_event(event_id)
    return {"detail": "event opened successfully"}
