from fastapi import HTTPException

from database import Event
from schemas.event import CreateEvent, UpdateEvent
from schemas.user import CreateUser, UpdateUser


class EventService:
    @staticmethod
    def create_event(new_event:CreateEvent):
        event_id = len(Event)+1
        event_data = new_event.model_dump()
        event_data["event_id"] = event_id
        event_data["is_open"] = True
        Event[event_id] = event_data
        return event_data

    @staticmethod
    def get_event(event_id:int):
        if event_id not in Event:
            raise HTTPException(status_code=404, detail="event not found")
        return Event[event_id]

    @staticmethod
    def get_event_title(title : str):
        for values in Event.values():
            if values["title"] == title:
                return values
        raise HTTPException(status_code=404, detail="event not found")

    @staticmethod
    def update_event(event_id: int, update_event : UpdateEvent):
        if event_id not in Event:
            raise HTTPException(status_code=404, detail="event not found")
        event= Event[event_id]
        if update_event.title is not None:
            event["title"] = update_event.title
        if update_event.location is not None:
            event["location"] = update_event.location
        if update_event.date is not None:
            event["date"] = update_event.date

        return event
    @staticmethod
    def delete_event(event_id:int):
        if event_id not in Event:
            raise HTTPException(status_code=404, detail="Event not found")
        del Event[event_id]

    @staticmethod
    def close_event(event_id:int):
        if event_id not in Event:
            raise HTTPException(status_code=404, detail="event not found")
        event = Event[event_id]

        if not event.get("is_open", True):
            raise HTTPException(status_code=400, detail="event is already closed")

        event["is_open"] = False
        return event

    @staticmethod
    def open_event(event_id: int):
        if event_id not in Event:
            raise HTTPException(status_code=404, detail="event not found")
        event = Event[event_id]

        if event.get("is_open", False):
            raise HTTPException(status_code=400, detail="event is already open")

        event["is_open"] = True
        return event






