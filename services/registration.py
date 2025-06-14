from typing import Dict

from fastapi import HTTPException

from database import User, Event, Registrations
from schemas.registration import RegisterUser

registration_id_counter = 1

class RegistrationService:

    @staticmethod
    def register_user(register: RegisterUser) -> dict:
        global registration_id_counter

        user_id = register.user_id
        event_id = register.event_id


        if user_id not in User:
            raise HTTPException(status_code=404, detail="User not found")
        if not User[user_id].get("is_active"):
            raise HTTPException(status_code=403, detail="User is inactive and cannot register for events")


        if event_id not in Event:
            raise HTTPException(status_code=404, detail="Event does not exist")
        if not Event[event_id].get("is_open"):
            raise HTTPException(status_code=403, detail="Event is not open for registration")

        for reg in Registrations.values():
            if reg["user_id"] == user_id and reg["event_id"] == event_id:
                raise HTTPException(status_code=400, detail="User already registered for this event")

        registration_data = register.model_dump()
        registration_data["registration_id"] = registration_id_counter
        registration_data["attended"] = False
        Registrations[registration_id_counter] = registration_data
        registration_id_counter += 1

        return registration_data

    @staticmethod
    def mark_attendance(registration_id:int):
        if registration_id not in Registrations:
            raise HTTPException(status_code=404, detail="event not found")
        registration = Registrations[registration_id]

        if registration.get("attended"):
            raise HTTPException(status_code=400, detail="User is already present")
        registration["attended"] = True
        return {"detail" : f"user{Registrations[registration_id]["user_id"]} marked present!"}

    @staticmethod
    def get_registered_events(user_id:int):
            if user_id not in User:
                raise HTTPException(status_code=404, detail="User not found")

            user_registrations = [
                reg for reg in Registrations.values() if reg["user_id"] == user_id
            ]

            return {"user_id": user_id, "registrations": user_registrations}

    @staticmethod
    def list_users_who_attended():
        attended_users = set()
        for registration_value in Registrations.values():
            if registration_value["attended"]:
                user_id = registration_value["user_id"]
                attended_users.add(f"user{user_id}")
        return attended_users
