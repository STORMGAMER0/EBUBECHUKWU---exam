from typing import Dict

from fastapi import APIRouter, status


from database import Registrations
from schemas.registration import ResponseRegistration, RegisterUser
from services.registration import RegistrationService
registration_router = APIRouter()

@registration_router.post("/registrations/", status_code=status.HTTP_201_CREATED, response_model= ResponseRegistration)
def register_new_user(register: RegisterUser):
    return RegistrationService.register_user(register)

@registration_router.get("/registrations", status_code=status.HTTP_200_OK,response_model=Dict[int, ResponseRegistration])
def get_registrations():
    return Registrations

@registration_router.put("/registrations/{registration_id}/attend", status_code=status.HTTP_200_OK)
def mark_attended(registration_id : int):
    return RegistrationService.mark_attendance(registration_id)

@registration_router.get("/registrations/user/{user_id}", status_code=status.HTTP_200_OK)
def get_user_registrations(user_id:int):
    return RegistrationService.get_registered_events(user_id)

